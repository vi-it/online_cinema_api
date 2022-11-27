"""
This module stores fixtures for pytest.
"""
import aiohttp
import aioredis
import asyncio
import http

import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from pytest_factoryboy import register
import factory

from tests.functional.factories import (FilmsFactory, PersonsFactory,
                                        GenresFactory)
from tests.functional.settings import test_settings
from tests.functional.testdata.es_mapping import EST_INDEXES
from tests.functional.utils.helpers import get_es_bulk_query
from tests.functional.utils.models import HTTPResponse

register(FilmsFactory)
register(PersonsFactory)
register(GenresFactory)


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='function')
async def es_client():
    client = AsyncElasticsearch(
        hosts=f'http://{test_settings.es_host}:{test_settings.es_port}'
    )
    yield client
    await client.close()


@pytest_asyncio.fixture(scope="function")
async def redis_client():
    client = await aioredis.create_redis_pool(
        (test_settings.redis_host, test_settings.redis_port),
        minsize=1,
        maxsize=20
    )
    yield client
    client.close()
    await client.wait_closed()


@pytest_asyncio.fixture(scope='function')
async def session():
    async with aiohttp.ClientSession() as session:
        yield session
    await session.close()


@pytest_asyncio.fixture
def create_es_index(es_client: AsyncElasticsearch):
    async def inner(index_name: str):
        await es_client.indices.create(
            index=index_name,
            body=EST_INDEXES[index_name],
            ignore=http.HTTPStatus.BAD_REQUEST
        )

    return inner


@pytest_asyncio.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict], index_name: str, es_id_field: str):
        bulk_query = get_es_bulk_query(data, index_name, es_id_field)
        str_query = '\n'.join(bulk_query) + '\n'

        response = await es_client.bulk(
            str_query,
            refresh='wait_for',  # wait till data is visible in search
        )
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


@pytest_asyncio.fixture
def storages_clean(es_client: AsyncElasticsearch,
                   redis_client: aioredis.Redis):
    async def inner(index_name: str):
        await redis_client.flushall()
        if await es_client.indices.exists(index=index_name):
            await es_client.indices.delete(index=index_name)

    return inner


@pytest_asyncio.fixture
def make_get_request(session: aiohttp.ClientSession):
    async def inner(url: str, query_data: str | None = None):
        url = (f'http://{test_settings.service_host}:'
               f'{test_settings.service_port}'
               f'/api/v1/{url}')
        async with session.get(url, params=query_data) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            return HTTPResponse(body=body, headers=headers, status=status)

    return inner


@pytest_asyncio.fixture
def upload_data_to_es_index(create_es_index, es_write_data, storages_clean):
    async def inner(quantity: int,
                    obj_factory: factory.Factory,
                    index_name: str,
                    es_id_field: str):
        objects = obj_factory.create_batch(quantity)
        await create_es_index(index_name=index_name)
        await es_write_data(data=[object.dict() for object in objects],
                            index_name=index_name,
                            es_id_field=es_id_field)
        yield objects
        await storages_clean(index_name)

    return inner
