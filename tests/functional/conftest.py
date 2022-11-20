"""
This module stores fixtures for pytest.
"""

import pytest
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='127.0.0.1:9200')
    yield client
    await client.close()


@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict]):
        bulk_query = get_es_bulk_query(data, test_settings.es_index, test_settings.es_id_field)
        str_query = '\n'.join(bulk_query) + '\n'

        response = await es_client.bulk(str_query, refresh=True)

        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


async def test_search(make_get_request, es_write_data, es_data: list[dict],
                      query_data: dict, expected_answer: dict):
    await es_write_data(es_data)
    response = await make_get_request('/search', query_data)
    # Дальше идут проверки ответа API
