"""
This module stores fixtures for pytest.
"""
import aiohttp
import asyncio

import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings
from tests.functional.utils.helpers import get_es_bulk_query
from tests.functional.utils.models import HTTPResponse


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='function')
async def es_client():
    client = AsyncElasticsearch(hosts=f'http://{test_settings.es_host}:{test_settings.es_port}')
    yield client
    await client.close()

@pytest_asyncio.fixture(scope='function')
async def session():
    async with aiohttp.ClientSession() as session:
        yield session
    await session.close()

@pytest_asyncio.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict], index_name: str, es_id_field: str):
        bulk_query = get_es_bulk_query(data, index_name, es_id_field)
        str_query = '\n'.join(bulk_query) + '\n'

        response = await es_client.bulk(str_query, refresh=True)
        await es_client.close()
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner

@pytest_asyncio.fixture
def make_get_request(session: aiohttp.ClientSession):
    async def inner(url: str, query_data):
        url = f'http://{test_settings.service_host}:{test_settings.service_port}' \
              f'/api/v1/{url}'
        async with session.get(url, params=query_data) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            return HTTPResponse(body=body, headers=headers, status=status)

    return inner
