# from functools import lru_cache
# from typing import Optional
#
# from aioredis import Redis
# from elasticsearch import AsyncElasticsearch
# from fastapi import Depends
#
# from src.core.config import (ES_INDEX_MOVIES, ES_INDEX_PERSONS,
#                              PERSON_CACHE_EXPIRE_IN_SECONDS)
# from src.db.elastic import get_elastic
# from src.db.redis import get_redis
# from src.models.film import Film
# from src.models.person import Person
#
#
# class PersonService:
#     def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
#         self.redis = redis
#         self.elastic = elastic
#         self.index = ES_INDEX_PERSONS
#
#     async def get_by_id(self, person_id: str) -> Optional[Person]:
#         """
#         Метод получения персоны по id из Redis или Elasticsearch.
#         :param person_id: id персоны
#         :return:
#         """
#         person = await self._person_from_cache(person_id)
#         if not person:
#             person = await self._get_person_from_elastic(person_id)
#             if not person:
#                 return None
#             await self._put_person_to_cache(person)
#
#         return person
#
#     async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
#         """
#         Метод получения персоны по id из Elasticsearch.
#         :param person_id: id персоны
#         :return:
#         """
#         doc = await self.elastic.get(self.index, person_id)
#         if not doc:
#             return
#         return Person(id=doc['_source'].get('id'),
#                       full_name=doc['_source'].get('name'),
#                       role=doc['_source'].get('role'),
#                       film_ids=doc['_source'].get('film_ids'))
#
#     async def _person_from_cache(self, person_id: str) -> Optional[Person]:
#         """
#         Метод получения персоны по id из Redis.
#         :param person_id: id персоны
#         :return:
#         """
#         data = await self.redis.get(person_id)
#         if not data:
#             return
#         person = Person.parse_raw(data)
#         return person
#
#     async def _put_person_to_cache(self, person: Person):
#         """
#         Метод записи персоны по id в Redis.
#         :param person: персона
#         :return:
#         """
#         await self.redis.set(str(person.id),
#                              person.json(),
#                              expire=PERSON_CACHE_EXPIRE_IN_SECONDS)
#
#     async def get_films_by_person(self,
#                                   person_id: str,
#                                   page_size: int,
#                                   page_number: int) -> list[Film]:
#         """
#         Метод получения фильмов персоны из Elasticsearch.
#         :param person_id: id персоны
#         :param page_size: размер страницы
#         :param page_number: номер страницы
#         :return:
#         """
#         roles = ['directors', 'actors', 'writers']
#
#         body = {
#             'size': page_size,
#             'from': (page_number - 1) * page_size,
#             'query': {
#                 'bool': {
#                     'should': []
#                 }
#             }
#         }
#         for role in roles:
#             body['query']['bool']['should'].append(
#                 {
#                     "nested": {
#                         "path": role,
#                         "query": {
#                             "bool": {
#                                 "filter": {
#                                     "match": {
#                                         role + ".id": person_id
#                                     }
#                                 }
#                             }
#                         }
#                     }
#                 }
#             )
#         doc = await self.elastic.search(index=ES_INDEX_MOVIES, body=body)
#         films = [Film(**item['_source']) for item in doc['hits']['hits']]
#         return films
#
#     async def search(self,
#                      query: str,
#                      page_size: int,
#                      page_number: int) -> list[Person]:
#         """
#         Метод получения персоны по поисковому запросу из Elasticsearch.
#         :param person_id: id персоны
#         :param page_size: размер страницы
#         :param page_number: номер страницы
#         :return:
#         """
#         body = {
#             'size': page_size,
#             'from': (page_number - 1) * page_size,
#             'query': {
#                 'simple_query_string': {
#                     "query": query,
#                     "default_operator": "and"
#                 }
#             }
#         }
#         doc = await self.elastic.search(index=self.index,
#                                         body=body)
#         persons = [Person(id=item['_source'].get('id'),
#                           full_name=item['_source'].get('name'),
#                           role=item['_source'].get('role'),
#                           film_ids=item['_source'].get('film_ids'))
#                    for item in doc['hits']['hits']]
#         return persons
#
#
# @lru_cache()
# def get_person_service(
#         redis: Redis = Depends(get_redis),
#         elastic: AsyncElasticsearch = Depends(get_elastic),
# ) -> PersonService:
#     return PersonService(redis, elastic)
