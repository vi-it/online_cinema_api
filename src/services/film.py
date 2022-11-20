"""
This module contains the asynchronous FilmService.
"""

from functools import lru_cache

from fastapi import Depends

from src.core.config import settings
from src.models import Film
from src.services._service_elt import ELTService
from src.services.cache import RedisCache, get_redis_extended
from src.services.storage import ElasticStorage, get_elastic_extended


class FilmService(ELTService):
    """
    A service that requests film data from Elasticsearch and wraps it in a
    model.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the class.
        """
        super().__init__(*args, **kwargs)
        self._model = Film
        self._cache_expire = settings.FILM_CACHE_EXPIRE_IN_SECONDS
        self._index = settings.ES_INDEX_MOVIES


@lru_cache()
def get_film_service(
        redis: RedisCache = Depends(get_redis_extended),
        elastic: ElasticStorage = Depends(get_elastic_extended),
) -> FilmService:
    """
    Return the service that retrieves film data as a singleton.

    Due to lru_caching the first call to the function instantiates the service,
    and all subsequent calls to the function are handled by the same instance
    of that service.
    """
    return FilmService(redis, elastic)
