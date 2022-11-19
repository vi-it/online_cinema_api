"""
This module is used by Docker Compose to find out if Redis is okay.
"""
import asyncio

import aioredis

from tests.functional.settings import test_settings


async def wait_redis():
    """
    Wait until Redis answers to ping(). The function is used to
    check if Redis is okay.
    """
    redis = await aioredis.create_redis(f'redis://{test_settings.redis_host}')
    response = await redis.ping()
    while not response:
        await asyncio.sleep(2)
        response = await redis.ping()


if __name__ == "__main__":
    asyncio.run(wait_redis())
