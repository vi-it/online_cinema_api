"""
This module contains the base asynchronous ELTService and its abstract class.
"""

import abc
import re
import sys

import elasticsearch
from aioredis import Redis

from src.core.config import settings


class ELTServiceProtocol(abc.ABC):
    """An abstract class for ELTService."""

    @abc.abstractmethod
    def __init__(self,
                 redis: Redis,
                 elastic: elasticsearch.AsyncElasticsearch) -> None:
        pass

    ##############################################
    #  Properties
    ##############################################

    @property
    @abc.abstractmethod
    def redis(self) -> Redis: ...

    @property
    @abc.abstractmethod
    def elastic(self) -> elasticsearch.AsyncElasticsearch: ...

    @property
    @abc.abstractmethod
    def model(self) -> settings.CINEMA_MODEL: ...

    @property
    @abc.abstractmethod
    def index(self) -> str: ...

    ##############################################
    # Public Methods
    ##############################################

    @abc.abstractmethod
    async def get_by_id(self,
                        object_id: str,
                        url: str) -> settings.CINEMA_MODEL | None: ...

    @abc.abstractmethod
    async def get_many(self, url: str,
                       page_size: int,
                       page_number: int) -> list[settings.CINEMA_MODEL] | list:
        ...

    @abc.abstractmethod
    async def search(
            self,
            query: str,
            page_size: int,
            page_number: int,
    ) -> list[settings.CINEMA_MODEL] | list: ...

    @abc.abstractmethod
    async def _get_from_elastic(
            self, object_id: str) -> settings.CINEMA_MODEL | None: ...

    @abc.abstractmethod
    async def _get_from_cache(
            self, object_id: str) -> settings.CINEMA_MODEL | None: ...

    @abc.abstractmethod
    async def _put_to_cache(self, item: settings.CINEMA_MODEL) -> None: ...

    ##############################################
    # Protected Methods
    ##############################################

    @abc.abstractmethod
    def _get_index(self, url: str) -> None: ...


class ELTService(ELTServiceProtocol):
    """
    Parent Service that requests data from an Elasticsearch index and wraps it
    in a cinema model. The Service contains implementation of methods common to
    all models. Methods specific to certain models are implemented in derived
    classes.
    """

    def __init__(self,
                 redis: Redis = Redis,
                 elastic: elasticsearch.AsyncElasticsearch =
                 elasticsearch.AsyncElasticsearch,
                 ) -> None:
        """
        Initialize the class.

        :param redis: Redis connections for retrieving data from caching
        :param elastic: Elasticsearch connection for requesting data
        """
        super().__init__(redis, elastic)
        self._redis = redis
        self._elastic = elastic
        self._model = None
        self._index = None

    @property
    def redis(self) -> Redis:
        """Return the Redis connection."""
        return self._redis

    @property
    def elastic(self) -> elasticsearch.AsyncElasticsearch:
        """Return the Elasticsearch connection."""
        return self._elastic

    @property
    def model(self) -> settings.CINEMA_MODEL:
        """Return the model class used for wrapping the API response."""
        return self._model

    @property
    def index(self) -> str:
        """Return the Elasticsearch index that is being requested."""
        return self._index

    def _get_index(self, url: str) -> None:
        """Retrieve the Elasticsearch index to be requested."""
        key = re.split('/{1,2}', url)[4]
        self._index = settings.ES_INDEXES[key][0]
        self._model = getattr(sys.modules['src.models'],
                              settings.ES_INDEXES[key][1])

    async def get_by_id(self,
                        object_id: str,
                        url: str) -> settings.CINEMA_MODEL | None:
        """
        Get the object by id from Redis or Elasticsearch.

        :param object_id: id
        :param url: URL to specify the Elasticsearch index.
        :return: cinema model or None
        """
        if not self._model or not self._index:
            self._get_index(url)
        obj = await self._get_from_cache(object_id)
        if not obj:
            obj = await self._get_from_elastic(object_id)
            if not obj:
                return None
            await self._put_to_cache(obj)
        return obj

    async def get_many(self, url: str,
                       page_size: int,
                       page_number: int) -> list[settings.CINEMA_MODEL] | list:
        """
        GET a list of objects from Elasticsearch given page size and number.

        :param url: URL to specify the target Elasticsearch index
        :param page_size:
        :param page_number:
        :return: a list of requested cinema objects (or empty list in case
            the response is empty)
        """
        if not self._model or not self._index:
            self._get_index(url)
        doc = await self._elastic.search(
            index=self._index, from_=(page_number - 1) * page_size,
            size=page_size,
        )
        res = [self._model(**x['_source']) for x in doc['hits']['hits']]
        return res

    async def search(
            self,
            query: str,
            page_size: int,
            page_number: int,
    ) -> list[settings.CINEMA_MODEL] | list:
        """
        GET objects from Elasticsearch according to the user's request.

        :param query: search query
        :param page_number: page number
        :param page_size: page size
        :return: a list of requested cinema objects (or empty list in case
            the response is empty)
        """
        body = {
            'size': page_size,
            'from': (page_number - 1) * page_size,
            'query': {
                'simple_query_string': {
                    'query': query,
                    'default_operator': 'and'
                }
            }
        }
        doc = await self._elastic.search(index=self._index, body=body)
        res = [self._model(**x['_source']) for x in doc['hits']['hits']]
        return res

    async def _get_from_elastic(
            self, object_id: str) -> settings.CINEMA_MODEL | None:
        """
        Handle the request to Elasticsearch based on object's id.

        :param object_id: id
        :return: cinema model or None
        """
        try:
            doc = await self._elastic.get(self._index, object_id)
        except elasticsearch.NotFoundError:
            return
        return self._model(**doc['_source'])

    async def _get_from_cache(self,
                              object_id: str) -> settings.CINEMA_MODEL | None:
        """
        Handle the request to Redis cache based on object's id.

        :param object_id: id персоны
        :return: cinema model or None
        """
        data = await self._redis.get(object_id)
        if not data:
            return None
        obj = self._model.parse_raw(data)
        return obj

    async def _put_to_cache(self, item: settings.CINEMA_MODEL) -> None:
        """
        Put the object to Redis cache based on its id.

        :param item: person
        :return: None
        """
        row = item.json()
        if self._index == 'persons':
            row = row.replace('full_name', 'name')
        await self._redis.set(
            item.id, row, expire=settings.CACHE_EXPIRE_IN_SECONDS,
        )
