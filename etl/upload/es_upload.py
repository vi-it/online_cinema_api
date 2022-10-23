import logging
import os
import typing

from transform import Filmwork

import elasticsearch
import elasticsearch.helpers

class ElasticsearchLoader:

    def __init__(self):
        self._es_host = os.environ.get('ES_HOST')
        self._es_port = os.environ.get('ES_PORT')
        self.es = elasticsearch.Elasticsearch(f"http://{self._es_host}:{self._es_port}", verify_certs=False,
                                              )

    def upload_data(self, data: typing.List[Filmwork]):
        # for r in data:
        #     print(r.dict())
        print(data)
        print(type(data))
        query = [{'_index': 'movies', '_id': data.id, '_source': dict(data)}]
        # query = [{'_index': 'movies', '_id': fw.id, '_source': fw.dict()} for fw in data]
        rows_count, errors = elasticsearch.helpers.bulk(self.es, query)

        if errors:
            logging.exception(f'Elasticsearch uploading error: {errors}')
        else:
            logging.info('Successfully uploaded {rows_count} rows.')

