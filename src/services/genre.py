from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.core.config import (ES_INDEX_GENRES, ES_SIZE,
                             GENRE_CACHE_EXPIRE_IN_SECONDS)
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.genre import Genre


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = ES_INDEX_GENRES

    async def get_by_id(self, genre_id: str):
        """
        Метод получения жанра по id из Redis или Elasticsearch.
        :param genre_id: id жанра
        :return:
        """
        genre = await self._get_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return
            await self._put_genre_to_cache(genre)

        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        """
        Метод получения жанра по id из Elasticsearch.
        :param genre_id: id жанра
        :return:
        """
        doc = await self.elastic.get(self.index, genre_id)
        return Genre(**doc['_source'])

    async def _get_from_cache(self, genre_id: str) -> Optional[Genre]:
        """
        Метод получения жанра по id из Redis.
        :param genre_id: id жанра
        :return:
        """
        data = await self.redis.get(genre_id)
        if not data:
            return
        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        """
        Метод записи жанра по id в Redis.
        :param genre: жанр
        :return:
        """
        await self.redis.set(str(genre.id),
                             genre.json(),
                             expire=GENRE_CACHE_EXPIRE_IN_SECONDS)

    async def get_list(self) -> list[Genre]:
        """
        Метод получения списка жанров из Elasticsearch.
        :return:
        """
        doc = await self.elastic.search(index=self.index, size=ES_SIZE)
        list_genres = [Genre(**x['_source']) for x in doc['hits']['hits']]
        return list_genres


@lru_cache()
def get_genre(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
