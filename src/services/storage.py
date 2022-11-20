"""
This module contains the classes implement Storage.
"""

import abc
from typing import Any

from elasticsearch import AsyncElasticsearch

from src.db.elastic import get_elastic


class StorageAbstract(abc.ABC):
    """An abstract class for storage with fulltext search interface."""

    @abc.abstractmethod
    async def get(self, *args, **kwargs) -> Any:
        """Get the object by id."""
        ...

    @abc.abstractmethod
    async def search(self, *args, **kwargs):
        """Get relevant objects"""
        ...


class ElasticStorage(StorageAbstract):
    def __init__(self, elastic: AsyncElasticsearch) -> None:
        self._elastic = elastic

    async def get(self, *args, **kwargs) -> Any:
        data = await self._elastic.get(*args, **kwargs)
        return data

    async def search(self, *args, **kwargs) -> Any:
        docs = await self._elastic.search(*args, **kwargs)
        return docs


async def get_elastic_extended() -> ElasticStorage:
    elastic = await get_elastic()
    return ElasticStorage(elastic)
