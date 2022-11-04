"""
Main script for running the program.
"""
import logging
import time

import transform
import upload
from extract import PostgresExtractor
from settings.setting_base import DELAY

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PostgresToElastic:
    """
    Handle extracting data from PostgreSQL, transforming it into
    Pydantic models, serializing and loading to the 'movies' index
    to Elasticsearch.
    """

    def process_data(self) -> None:
        """Run the process."""
        extractor = PostgresExtractor()
        for index, index_mapper in upload.EST_INDEXES.items():
            transformer = transform.Transform(index)
            loader = upload.ElasticsearchLoader(index)
            for raw_data in extractor.extract(index):
                for row in raw_data:
                    obj = transformer.transform(row)
                    logger.info(obj)
                    loader.upload_data(obj)


def main_func():
    """Main utility function for starting the data transfer."""
    pg_to_es = PostgresToElastic()
    while True:
        pg_to_es.process_data()
        time.sleep(DELAY)


if __name__ == '__main__':
    main_func()
