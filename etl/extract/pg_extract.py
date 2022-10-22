import os
import logging
from contextlib import closing, contextmanager

import psycopg2

from utils import JsonFileStorage, State
from extract_query import EXTRACT_QUERY

class PostgresExtractor:
    """
    A class for extracting data from a PostgreSQL database.
    """

    def __init__(self, chunk: int):
        self.chunk = chunk
        self.modified = ...
        self.state = ...

    def _connect(self):
        auth = {'dbname': os.environ.get('DB_NAME'), 'user': os.environ.get('DB_USER'),
                'password': os.environ.get('DB_PASSWORD'), 'host': os.environ.get('DB_HOST'),
                'port': os.environ.get('DB_PORT'), 'options': '-c search_path=content'}
        try:
            cursor = psycopg2.connect(**auth, cursor_factory=DictCursor)
            return cursor
        except psycopg2.OperationalError:
            logging.exception("Database transfer failed. Could not connect to the database server!")
        except Exception as error:
            logging.exception(f"Database transfer failed. The following exception came up: {error}")

    def extract(self):

        with closing(self._connect()) as pg_cursor:
            with open('extract_query') as query_file:
                query = query_file.read()

        pg_cursor.execute(query, (self.modified, self.modified, self.modified))

        while data := pg_cursor.fetchmany(self.chunk):
            self.state.save_key('pg_state', data)
            logging.info("Extracted film data from PostgreSQL")
            yield data
            self.sate.save_key('pg_state', None)
