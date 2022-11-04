import datetime
import logging
from contextlib import closing

import psycopg2
from psycopg2.extras import DictCursor

import settings
from backoff import backoff
from utils import JsonFileStorage, State

from .extract_query import (EXTRACT_QUERY_FILM, EXTRACT_QUERY_GENRES,
                            EXTRACT_QUERY_PERSONS)

logger = logging.getLogger(__name__)


class PostgresExtractor:
    """
    A class for extracting data from a PostgreSQL database.
    """

    def __init__(self) -> None:
        self.state = State(JsonFileStorage('state.json'))
        self.essence = None
        self.queries = {
            'movies': EXTRACT_QUERY_FILM,
            'persons': EXTRACT_QUERY_PERSONS,
            'genres': EXTRACT_QUERY_GENRES
        }

    def _modified(self) -> str:
        """
        Define the last time the data was retrieved to be able
        to update only the records that have been changed since then.
        """
        modified = self.state.get_state(f'pg_state_{self.essence}')
        if modified is None:
            modified = datetime.datetime.min.strftime('%Y-%m-%d %H:%M:%S')
        else:
            modified = self.state.get_state(f'pg_modified_{self.essence}')
        return modified

    @backoff(exceptions=(psycopg2.OperationalError,))
    def _connect(self) -> psycopg2.extras.DictCursor:
        """Establish the database connection to PostgreSQL."""
        connection = psycopg2.connect(**settings.PG, cursor_factory=DictCursor)
        return connection.cursor()

    @backoff(exceptions=(AttributeError,))
    def extract(self, essence: str, chunk: int = 100) -> list | None:
        """
        Extract and yield database data by piece. If the processing had been
        interrupted before, yield the previously loaded data. Update the
        state of execution.
        """
        self.essence = essence
        pg_state = self.state.get_state(f'pg_state_{self.essence}')
        query = self.queries[essence]

        if pg_state is not None:
            yield pg_state
        try:
            with closing(self._connect()) as pg_cursor:
                params = (
                    (self._modified(),) * 3
                    if essence == 'movies'
                    else (self._modified(),)
                )
                pg_cursor.execute(query, params)

                while data := pg_cursor.fetchmany(chunk):
                    self.state.set_state(f'pg_state_{self.essence}', data)
                    self.state.set_state(f'pg_modified_{self.essence}', self._modified())
                    logger.info("Extracted {} data from PostgreSQL".format(essence))

                    yield data

                    self.state.set_state(f'pg_state_{self.essence}', None)
                self.state.set_state(f'pg_state_{self.essence}', None)
        except AttributeError as e:
            logger.exception('Can\'t close the database connection.'
                             'Seems that the database connection is'
                             'no longer functioning: {}'.format(e))
        except Exception as e:
            logger.exception('ERROR: {}'.format(e))
