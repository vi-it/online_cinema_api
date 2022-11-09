from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.core.config import settings
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.film import Film
from src.services.service_elt import ELTService


class PersonService(ELTService):
    """
    Сервис, запрошивающий данные о персонах из индекса Elasticsearch и
    возвращающий их в виде объекта(-ов) одной из моделей онлайн-кинотеатра.
    """

    async def get_films_by_person(self,
                                  person_id: str,
                                  page_size: int,
                                  page_number: int) -> list[Film]:
        """
        Метод получения фильмов персоны из Elasticsearch.
        :param person_id: id персоны
        :param page_size: размер страницы
        :param page_number: номер страницы
        :return:
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
        doc = await self.elastic.search(index=settings.ES_INDEX_MOVIES,
                                        body=body)
        films = [Film(**item['_source']) for item in doc['hits']['hits']]
        return films


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
