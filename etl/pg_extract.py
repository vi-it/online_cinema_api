import os
import logging
from contextlib import closing, contextmanager

import psycopg2


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
            query = """
            SELECT
               fw.id,
               fw.title,
               fw.description,
               fw.rating,
               fw.type,
               fw.created,
               fw.modified,
               COALESCE (
                   json_agg(
                       DISTINCT jsonb_build_object(
                           'person_role', pfw.role,
                           'person_id', p.id,
                           'person_name', p.full_name
                       )
                   ) FILTER (WHERE p.id is not null),
                   '[]'
               ) as persons,
               array_agg(DISTINCT g.name) as genres
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            WHERE fw.modified > %s OR 
            g.modified > %s OR 
            p.modified > %s
            GROUP BY fw.id
            ORDER BY fw.modified;
            """

            pg_cursor.execute(query, (self.modified, self.modified, self.modified))

            while data := pg_cursor.fetchmany(self.chunk):
                self.state.save_key('pg_state', data)
                logging.info("Extracted film data from PostgreSQL")
                yield data
                self.sate.save_key('pg_state', None)
