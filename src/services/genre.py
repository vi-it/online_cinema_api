from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.core.config import settings
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models import Genre
from src.services._service_elt import ELTService


class GenreService(ELTService):
    """
    Сервис, запрошивающий данные о жанрах из индекса Elasticsearch и
    возвращающий их в виде объекта(-ов) одной из моделей онлайн-кинотеатра.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model = Genre
        self._index = settings.ES_INDEX_GENRES


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
