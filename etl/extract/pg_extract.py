import datetime
import os
import logging
from contextlib import closing

import psycopg2
from psycopg2.extras import DictCursor

from utils import JsonFileStorage, State
from .extract_query import EXTRACT_QUERY

class PostgresExtractor:
    """
    A class for extracting data from a PostgreSQL database.
    """

    def __init__(self):
        self.state = State(JsonFileStorage('state.json'))

    def _modified(self):
        modified = self.state.get_state('pg_modified')
        if not modified:
            modified = datetime.datetime.min.strftime('%Y-%m-%d %H:%M:%S')
        return modified

    def _connect(self):
        auth = {'dbname': os.environ.get('DB_NAME'), 'user': os.environ.get('DB_USER'),
                'password': os.environ.get('DB_PASSWORD'), 'host': os.environ.get('DB_HOST'),
                'port': os.environ.get('DB_PORT'), 'options': '-c search_path=content'}
        try:
            connection = psycopg2.connect(**auth, cursor_factory=DictCursor)
            return connection.cursor()
        except psycopg2.OperationalError:
            logging.exception("Database transfer failed. Could not connect to the database server!")
        except Exception as error:
            logging.exception(f"Database transfer failed. The following exception came up: {error}")

    def extract(self, chunk: int = 100):
        pg_state = self.state.get_state('pg_state')

        if pg_state is not None:
            yield pg_state

        with closing(self._connect()) as pg_cursor:
            pg_cursor.execute(EXTRACT_QUERY, (self._modified(),)*3)

            while data := pg_cursor.fetchmany(chunk):
                self.state.set_state('pg_state', data)
                self.state.set_state('pg_modified', self._modified)
                logging.info("Extracted film data from PostgreSQL")

                yield data

                self.state.set_state('pg_state', None)
                self.state.set_state('pg_modified', None)
