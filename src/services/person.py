"""
This module contains the asynchronous PersonService and its abstract class.
"""

import abc
from functools import lru_cache

from fastapi import Depends

from src.core.config import settings
from src.models import Film, Person
from src.services._service_elt import ELTService
from src.services.cache import RedisCache, get_redis_extended
from src.services.storage import ElasticStorage, get_elastic_extended


class PersonServiceAbstract(abc.ABC):
    """An abstract class for methods specific to PersonService."""

    ##############################################
    # Public Methods
    ##############################################

    async def get_films_by_person(self,
                                  person_id: str,
                                  page_size: int,
                                  page_number: int) -> list[Film]: ...


class PersonService(ELTService, PersonServiceAbstract):
    """
    A service that requests person data from Elasticsearch and wraps it in a
    model.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model = Person
        self._index = settings.ES_INDEX_PERSONS
        self._cache_expire = settings.PERSON_CACHE_EXPIRE_IN_SECONDS

    async def get_films_by_person(self,
                                  person_id: str,
                                  page_size: int,
                                  page_number: int) -> list[Film]:
        """
        Return films filtered by person.

        :param person_id: person id
        :param page_size: size of the page
        :param page_number: number of the page
        :return: list of films
        """
        roles = ['directors', 'actors', 'writers']

        body = {
            'size': page_size,
            'from': (page_number - 1) * page_size,
            'query': {
                'bool': {
                    'should': []
                }
            }
        }
        for role in roles:
            body['query']['bool']['should'].append(
                {
                    "nested": {
                        "path": role,
                        "query": {
                            "bool": {
                                "filter": {
                                    "match": {
                                        role + ".id": person_id
                                    }
                                }
                            }
                        }
                    }
                }
            )
        doc = await self._elastic.search(index=settings.ES_INDEX_MOVIES,
                                         body=body)
        films = [Film(**item['_source']) for item in doc['hits']['hits']]
        return films


@lru_cache()
def get_person_service(
        redis: RedisCache = Depends(get_redis_extended),
        elastic: ElasticStorage = Depends(get_elastic_extended),
) -> PersonService:
    """
    Return the service that retrieves person data as a singleton.

    Due to lru_caching the first call to the function instantiates the service,
    and all subsequent calls to the function are handled by the same instance
    of that service.
    """
    return PersonService(redis, elastic)
