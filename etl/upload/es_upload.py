import logging
import typing

import elasticsearch
import elasticsearch.helpers

import settings
from backoff import backoff
from transform import Filmwork
from . import es_schema

class ElasticsearchLoader:
    """Load the movies data to the Elasticsearch index"""

    def __init__(self) -> None:
        self.es = elasticsearch.Elasticsearch(
            f"http://{settings.EST['es_host']}:{settings.EST['es_port']}",
            verify_certs=False
        )

    @backoff(exceptions=(elasticsearch.exceptions.ConnectionError))
    def upload_data(self, data: typing.List[Filmwork]) -> None:
        """Upload the data to the index 'moves'."""
        self.es.check_index()

        query = [{'_index': 'movies', '_id': data.id, '_source': dict(data)}]
        rows_count, errors = elasticsearch.helpers.bulk(self.es, query)

        if errors:
            logging.exception(f'Elasticsearch uploading error: {errors}'
                              f'while executing query {query}.')
        else:
            logging.info(f'Successfully uploaded {rows_count} rows.')

    @backoff(exceptions=(elasticsearch.exceptions.ConnectionError))
    def check_index(self, idx_name: str):
        if not self.exists(index=idx_name):
            self.es.indices.create(index=idx_name,
                                   body=es_schema.EST_REQUEST,
                                   ignore=400)

