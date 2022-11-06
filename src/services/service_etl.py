from functools import lru_cache
import typing

from aioredis import Redis
import elasticsearch
from fastapi import Depends
import pydantic

from src.core.config import CACHE_EXPIRE_IN_SECONDS
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src import models


CINEMA_MODEL = typing.TypeVar('CINEMA_MODEL',
                              models.Films, models.Person, models.Genre)

class ELTService:
    """
    Сервис, запрошивающий данные из индекса Elasticsearch и возвращающий их
    в виде объекта(-ов) одной из моделей онлайн-кинотеатра.
    """
    def __init__(self,
                 model: pydantic.main.ModelMetaclass,
                 redis: Redis = Redis,
                 elastic: elasticsearch.AsyncElasticsearch =
                 elasticsearch.AsyncElasticsearch
                 ) -> None:
        self.model = model
        self.index = self.model.alias
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, object_id: str) -> CINEMA_MODEL:
        """
        Получить объект по id из Redis или Elasticsearch.
        :param object_id: id
        :return: объект, относящийся к онлайн-кинотеатру
        """
        obj = await self._get_from_cache(object_id)
        if not obj:
            item = await self._get_from_elastic(object_id)
            if not obj:
                return None
            await self._put_to_cache(item)
        return obj

    async def search(self,
                     query: str,
                     page_number: int,
                     page_size: int = 20) -> list[CINEMA_MODEL]:
        """
        Получить объекты из Elasticsearch в соответствии с запросом
        пользователя.
        :param query: поисковой запрос
        :param page_number: номер страницы
        :param page_size: размер страницы
        :return: список объектов, относящихся к онлайн-кинотеатру
        """
        body = {
            'size': page_size,
            'from': (page_number - 1) * page_size,
            'query': {
                'simple_query_string': {
                    "query": query,
                    "default_operator": "and"
                }
            }
        }
        doc = await self.elastic.search(index=self.index, body=body)
        objects = pydantic.parse_obj_as(list[self.model], doc['hits']['hits'])
        return objects

    async def _get_from_elastic(self, object_id: str) -> CINEMA_MODEL:
        """
        Обработать запрос объекта по id из Elasticsearch.
        :param object_id: id персоны
        :return:
        """
        try:
            doc = await self.elastic.get(self.index, object_id)
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

        obj = self.model.parse_raw(data)
        return obj

    async def _put_to_cache(self, item):
        """
        Записать объект по id в Redis.
        :param item: персона
        :return:
        """
        await self.redis.set(item.id, item.json(),
                             expire=CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_elt_service(
        model: pydantic.main.ModelMetaclass,
        redis: Redis = Depends(get_redis),
        elastic: elasticsearch.AsyncElasticsearch = Depends(get_elastic),
) -> ELTService:
    return ELTService(model, redis, elastic)
