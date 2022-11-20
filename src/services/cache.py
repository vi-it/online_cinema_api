"""
This module contains the classes implement Cache.
"""

import abc
from typing import Any

from aioredis import Redis

from src.db.redis import get_redis


class CacheAbstract:
    """An abstract class for cache storage."""

    @abc.abstractmethod
    def client(self) -> Any:
        """Return client interface."""
        ...

    @abc.abstractmethod
    async def get(self, key: Any) -> Any:
        """Get the value of a key."""
        ...

    @abc.abstractmethod
    async def set(self, key: Any, value: Any, *args, **kwargs) -> Any:
        """Set the value of a key."""
        ...


class RedisCache(CacheAbstract):
    """Class Redit class."""

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def client(self) -> Redis | None:
        return self._redis

    async def get(self, key: Any) -> Any:
        data = await self._redis.get(key)
        return data

    async def set(self, key: Any, value: Any, *args, **kwargs) -> Any:
        await self._redis.set(key, value, *args, **kwargs)


async def get_redis_extended() -> RedisCache:
    redis = await get_redis()
    return RedisCache(redis)
