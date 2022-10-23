"""
Main script for running the program.
"""
import logging

import elasticsearch

import transform
import upload
from extract import PostgresExtractor


class PostgresToElastic:
    """
    Handle extracting data from PostgreSQL, transforming it into
    Pydantic models, serializing and loading to the 'movies' index
    to Elasticsearch.
    """

    def process_data(self) -> None:
        """Run the process."""
        extractor = PostgresExtractor()

        for raw_data in extractor.extract():
            for row in raw_data:
                fw = transform.Transform(row)
                film = fw.to_filmwork()

                logging.info(film)

                es_loader = upload.ElasticsearchLoader()
                es_loader.upload_data(film)


def main_func():
    """Main utility function for starting the data transfer."""
    pg_to_es = PostgresToElastic()
    pg_to_es.process_data()


if __name__ == '__main__':
    main_func()
