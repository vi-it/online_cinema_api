import datetime
import logging
import os
import typing
from contextlib import closing

import psycopg2
from psycopg2.extras import DictCursor

import settings
from .extract_query import EXTRACT_QUERY
from backoff import backoff
from utils import JsonFileStorage, State


class PostgresExtractor:
    """
    A class for extracting data from a PostgreSQL database.
    """

    def __init__(self) -> None:
        self.state = State(JsonFileStorage('state.json'))

    def _modified(self) -> str:
        """
        Define the last time the data was retrieved to be able
        to update only the records that have been changed since then.
        """
        modified = self.state.get_state('pg_modified')
        if modified is None:
            modified = datetime.datetime.min.strftime('%Y-%m-%d %H:%M:%S')
        else:
            modified = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return modified

    @backoff(exceptions=(psycopg2.OperationalError,))
    def _connect(self) -> psycopg2.extras.DictCursor:
        """Establish the database connection to PostgreSQL."""
        auth = settings.PGSettings().dict()
        connection = psycopg2.connect(**auth, cursor_factory=DictCursor)
        return connection.cursor()

    @backoff(exceptions=[AttributeError])
    def extract(self, chunk: int = 100) -> typing.Optional[list]:
        """
        Extract and yield database data by piece. If the processing had been
        interrupted before, yield the previously loaded data. Update the
        state of execution.
        """
        pg_state = self.state.get_state('pg_state')

        if pg_state is not None:
            yield pg_state
        try:
            with closing(self._connect()) as pg_cursor:
                pg_cursor.execute(EXTRACT_QUERY, (self._modified(),)*3)

                while data := pg_cursor.fetchmany(chunk):
                    self.state.set_state('pg_state', data)
                    self.state.set_state('pg_modified', self._modified())
                    logging.info("Extracted film data from PostgreSQL")

                    yield data

                    self.state.set_state('pg_state', None)
        except AttributeError as e:
            logging.exception(f"Can't close the database connection."
                              f"Seems that the database connection is"
                              f"no longer functioning: {e}")
        except Exception as e:
            logging.exception(f'ERROR: {e}')
