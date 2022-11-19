import os
import time

from elasticsearch import Elasticsearch

if __name__ == '__main__':
    host = os.getenv('ELASTIC_HOST', default='127.0.0.1')
    port = os.getenv('ELASTIC_PORT', default='9200')
    es_client = Elasticsearch(hosts=f'http://{host}:{port}', validate_cert=False, use_ssl=False)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
