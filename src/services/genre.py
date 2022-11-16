"""
This module contains the asynchronous GenreService.
"""

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
    A service that requests genre data from Elasticsearch and wraps it in a
    model.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the class.
        """
        super().__init__(*args, **kwargs)
        self._model = Genre
        self._index = settings.ES_INDEX_GENRES


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    """
    Return the service that retrieves genre data as a singleton.

    Due to lru_caching the first call to the function instantiates the service,
    and all subsequent calls to the function are handled by the same instance
    of that service.
    """
    return GenreService(redis, elastic)
