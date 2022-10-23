import logging
import typing

import elasticsearch
import elasticsearch.helpers

import settings
from backoff import backoff
from transform import Filmwork

class ElasticsearchLoader:
    """Load the movies data to the Elasticsearch index"""

    def __init__(self) -> None:
        self._auth = settings.EST().dict()
        self.es = elasticsearch.Elasticsearch(
            f"http://{self._auth['es_host']}:{self._auth['es_port']}",
            verify_certs=False
        )

    @backoff(exceptions=(elasticsearch.exceptions.ConnectionError))
    def upload_data(self, data: typing.List[Filmwork]) -> None:
        """Upload the data to the index 'moves'."""
        query = [{'_index': 'movies', '_id': data.id, '_source': dict(data)}]
        rows_count, errors = elasticsearch.helpers.bulk(self.es, query)

        if errors:
            logging.exception(f'Elasticsearch uploading error: {errors}'
                              f'while executing query {query}.')
        else:
            logging.info(f'Successfully uploaded {rows_count} rows.')

