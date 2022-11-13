import re
import sys
from functools import lru_cache

import elasticsearch
from aioredis import Redis
from fastapi import Depends

from src.core.config import settings
from src.db.elastic import get_elastic
from src.db.redis import get_redis


class ELTService:
    """
    Родительский сервис, запрошивающий данные из индекса Elasticsearch и
    возвращающий их в виде объекта(-ов) одной из моделей онлайн-кинотеатра.
    Содержит реализацию общих для всех сущностей методов. Методы, специфичные
    отдельным сущностям, реализуются в классах-наследниках.
    """
    def __init__(self,
                 redis: Redis = Redis,
                 elastic: elasticsearch.AsyncElasticsearch =
                 elasticsearch.AsyncElasticsearch
                 ) -> None:
        self.redis = redis
        self.elastic = elastic
        self.model = None
        self.index = None

    def get_index(self, url):
        key = re.split("/{1,2}", url)[4]
        self.index = settings.ES_INDEXES[key][0]
        self.model = getattr(sys.modules['src.models'], settings.ES_INDEXES[key][1])

    async def get_by_id(self,
                        object_id: str,
                        url: str) -> settings.CINEMA_MODEL | None:
        """
        Получить объект по id из Redis или Elasticsearch.
        :param object_id: id
        :return: объект, относящийся к онлайн-кинотеатру
        """
        if not self.model or not self.index:
            self.get_index(url)
        obj = await self._get_from_cache(object_id)
        if not obj:
            obj = await self._get_from_elastic(object_id)
            if not obj:
                return None
            await self._put_to_cache(obj)
        return obj

    async def get_many(self, url: str,
                       page_size: int,
                       page_number: int) -> list[settings.CINEMA_MODEL | None]:
        if not self.model or not self.index:
            self.get_index(url)
        doc = await self.elastic.search(
            index=self.index, from_=(page_number - 1) * page_size, size=page_size
        )
        res = [self.model(**x['_source']) for x in doc['hits']['hits']]
        return res

    async def search(
            self,
            query: str,
            page_size: int,
            page_number: int
    ) -> list[settings.CINEMA_MODEL]:
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
        res = [self.model(**x['_source']) for x in doc['hits']['hits']]
        return res

    async def _get_from_elastic(self, object_id: str) -> \
            settings.CINEMA_MODEL | None:
        """
        Обработать запрос объекта по id из Elasticsearch.
        :param object_id: id персоны
        :return:
        """
        try:
            doc = await self.elastic.get(self.index, object_id)
        except elasticsearch.NotFoundError:
            return
        return self.model(**doc['_source'])

    async def _get_from_cache(self, object_id: str):
        """
        Обработать запрос объекта по id из Redis.
        :param object_id: id персоны
        :return:
        """
        data = await self.redis.get(object_id)
        if not data:
            return
        obj = self.model.parse_raw(data)
        return obj

    async def _put_to_cache(self, item):
        """
        Записать объект по id в Redis.
        :param item: персона
        :return:
        """
        row = item.json()
        if self.index == 'persons':
            row = row.replace('full_name', 'name')
        await self.redis.set(item.id, row,
                             expire=settings.CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_elt_service(
        redis: Redis = Depends(get_redis),
        elastic: elasticsearch.AsyncElasticsearch = Depends(get_elastic),
) -> ELTService:
    return ELTService(redis, elastic)
