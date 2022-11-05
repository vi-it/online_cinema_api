from functools import lru_cache
import typing


from aioredis import Redis
import elasticsearch
from fastapi import Depends
import pydantic

from src.core.config import (ES_INDEX_MOVIES, ES_INDEX_PERSONS,
                             PERSON_CACHE_EXPIRE_IN_SECONDS)
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src import models
from src.core.config import FILM_CACHE_EXPIRE_IN_SECONDS


CINEMA_MODEL = typing.TypeVar('CINEMA_MODEL',
                              models.Films, models.Person, models.Genre)

class ELTService:
    """
    A service that requests data from Elasticsearch and wraps it in a Pydantic
    model.
    """
    def __init__(self,
                 index: str,
                 model: pydantic.main.ModelMetaclass,
                 redis: Redis = Redis,
                 elastic: elasticsearch.AsyncElasticsearch =
                 elasticsearch.AsyncElasticsearch
                 ) -> None:
        self.index = index
        self.model = model
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, object_id: str) -> CINEMA_MODEL:
        """
        Получить объект по id из Redis или Elasticsearch.
        :param object_id: id
        :return:
        """
        film = await self._get_from_cache(object_id)
        if not film:
            item = await self._get_from_elastic(object_id)
            if not film:
                return None
            await self._put_to_cache(item)

    async def search(self):
        pass

    async def _get_from_elastic(self, object_id: str) -> CINEMA_MODEL:
        """
        Обработать запрос объекта по id из Elasticsearch.
        :param object_id: id персоны
        :return:
        """
        try:
            doc = await self.elastic.get(self.model.alias, object_id)
        except elasticsearch.NotFoundError:
            return None
        return self.model(**doc['_source'])

    async def _get_from_cache(self, object_id: str):
        """
        Обработать запрос объекта по id из Redis.
        :param object_id: id персоны
        :return:
        """
        data = await self.redis.get(object_id)
        if not data:
            return None

        film = self.model.parse_raw(data)
        return film

    async def _put_to_cache(self, item):
        """
        Записать объект по id в Redis.
        :param item: персона
        :return:
        """
        await self.redis.set(item.id, item.json(),
                             expire=FILM_CACHE_EXPIRE_IN_SECONDS)

