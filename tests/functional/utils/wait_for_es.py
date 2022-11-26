"""
This module is used by Docker Compose to find out if Elasticsearch is okay.
"""

import logging.config  # noqa: WPS301
import os
import time

from elasticsearch import Elasticsearch

logging.config.fileConfig(
    fname='tests/functional/log.conf',
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)


def wait_elasticsearch():
    """
    Wait until Elasticsearch answers to ping(). The function is used to
    check if Elasticsearch is okay.
    """
    # os.getenv is used instead of pydantic's settings cause the module
    # is run as a stand-alone script
    host = os.getenv('ELASTIC_HOST', default='127.0.0.1')
    port = os.getenv('ELASTIC_PORT', default='9200')
    logger.info('Starting a check if Elasticsearch is up...')
    es_client = Elasticsearch(
        hosts=f'http://{host}:{port}',
        validate_cert=False,
        use_ssl=False,
    )
    attempt = 1
    while True:
        logger.info(f'Trying to ping Elasticsearch (attempt {attempt})...')
        if es_client.ping():
            logger.info('Elasticsearch is up!')
            es_client.close()
            break
        time.sleep(1)


if __name__ == '__main__':
    wait_elasticsearch()
