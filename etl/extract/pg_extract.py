import os
import logging
from contextlib import closing, contextmanager

import psycopg2

from utils import JsonFileStorage, State
from .extract_query import EXTRACT_QUERY

class PostgresExtractor:
    """
    A class for extracting data from a PostgreSQL database.
    """

    def __init__(self, chunk: int = 100):
        self.chunk = chunk
        self.state = State(JsonFileStorage('state.json'))
        self.modified = self.state.get_state('pg_state')

    def _connect(self):
        auth = {'dbname': os.environ.get('DB_NAME'), 'user': os.environ.get('DB_USER'),
                'password': os.environ.get('DB_PASSWORD'), 'host': os.environ.get('DB_HOST'),
                'port': os.environ.get('DB_PORT'), 'options': '-c search_path=content'}
        try:
            cursor = psycopg2.connect(**auth, cursor_factory=psycopg2.extras.DictCursor)
            return cursor
        except psycopg2.OperationalError:
            logging.exception("Database transfer failed. Could not connect to the database server!")
        except Exception as error:
            logging.exception(f"Database transfer failed. The following exception came up: {error}")

    def extract(self):

        with closing(self._connect()) as pg_cursor:
            pg_cursor.execute(EXTRACT_QUERY, (self.modified, self.modified, self.modified))

            while data := pg_cursor.fetchmany(self.chunk):
                self.state.save_key('pg_state', data)
                logging.info("Extracted film data from PostgreSQL")
                yield data
                self.sate.save_key('pg_state', None)
