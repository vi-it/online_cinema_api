from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.services.service_elt import ELTService


class FilmService(ELTService):
    """
    Сервис, запрошивающий данные о фильмах из индекса Elasticsearch и
    возвращающий их в виде объекта(-ов) одной из моделей онлайн-кинотеатра.
    """
    pass


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
