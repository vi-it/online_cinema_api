"""
This module is used by Docker Compose to find out if Elasticsearch is okay.
"""

import os
import time

from elasticsearch import Elasticsearch


def wait_elasticsearch():
    """
    Wait until Elasticsearch answers to ping(). The function is used to
    check if Elasticsearch is okay.
    """
    # os.getenv is used instead of pydantic's settings cause the module
    # is run a stand-alone scriptf
    host = os.getenv('ELASTIC_HOST', default='127.0.0.1')
    port = os.getenv('ELASTIC_PORT', default='9200')
    es_client = Elasticsearch(
        hosts=f'http://{host}:{port}',
        validate_cert=False,
        use_ssl=False,
    )
    while True:
        if es_client.ping():
            break
        time.sleep(1)


if __name__ == '__main__':
    wait_elasticsearch()
