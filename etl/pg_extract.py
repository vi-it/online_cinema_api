import os
import logging
from contextlib import closing, contextmanager

import psycopg2


class PostgresExtractor:
    """
    A class for extracting data from a PostgreSQL database.
    """

    def __init__(self):
        pass

    def _connect(self):
        auth = {'dbname': os.environ.get('DB_NAME'), 'user': os.environ.get('DB_USER'),
                'password': os.environ.get('DB_PASSWORD'), 'host': os.environ.get('DB_HOST'),
                'port': os.environ.get('DB_PORT'), 'options': '-c search_path=content'}
        try:
            with closing(psycopg2.connect(**auth, cursor_factory=DictCursor)) as pg_conn:
        except psycopg2.OperationalError:
            logging.exception("Database transfer failed. Could not connect to the database server!")
        except Exception as error:
            logging.exception(f"Database transfer failed. The following exception came up: {error}")


