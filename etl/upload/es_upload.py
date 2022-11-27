import http
import logging

import elasticsearch
import elasticsearch.helpers

import settings
from backoff import backoff
from transform import Filmwork

from .es_schema import EST_INDEXES

logger = logging.getLogger(__name__)


class ElasticsearchLoader:
    """Load the movies data to the Elasticsearch index"""

    def __init__(self, index) -> None:
        self.es = elasticsearch.Elasticsearch(
            f"http://{settings.EST['es_host']}:{settings.EST['es_port']}",
            verify_certs=False
        )
        self.index = index

    @backoff(exceptions=(elasticsearch.exceptions.ConnectionError,))
    def upload_data(self, data: list[Filmwork]) -> None:
        """Upload the data to the index."""
        self.check_index()

        query = [{'_index': self.index, '_id': data.id, '_source': dict(data)}]
        rows_count, errors = elasticsearch.helpers.bulk(self.es, query)

        if errors:
            logger.exception(f'Elasticsearch uploading error: {errors}'
                             f'while executing query {query}.')
        else:
            logger.info(f'Successfully uploaded {rows_count} rows.')

    @backoff(exceptions=(elasticsearch.exceptions.ConnectionError,))
    def check_index(self):
        if not self.es.indices.exists(index=self.index):
            logger.info(f"Create index - {self.index}.")
            self.es.indices.create(index=self.index,
                                   body=EST_INDEXES[self.index],
                                   ignore=http.HTTPStatus.BAD_REQUEST)
            return
        logger.info("Index {} is already created.".format(self.index))
