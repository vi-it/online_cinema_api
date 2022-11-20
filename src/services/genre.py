"""
This module contains the asynchronous GenreService.
"""

from functools import lru_cache

from fastapi import Depends

from src.core.config import settings
from src.models import Genre
from src.services._service_elt import ELTService
from src.services.cache import RedisCache, get_redis_extended
from src.services.storage import ElasticStorage, get_elastic_extended


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
        self._cache_expire = settings.GENRE_CACHE_EXPIRE_IN_SECONDS


@lru_cache()
def get_genre_service(
        redis: RedisCache = Depends(get_redis_extended),
        elastic: ElasticStorage = Depends(get_elastic_extended),
) -> GenreService:
    """
    Return the service that retrieves genre data as a singleton.

    Due to lru_caching the first call to the function instantiates the service,
    and all subsequent calls to the function are handled by the same instance
    of that service.
    """
    return GenreService(redis, elastic)
