"""
This module is used by Docker Compose to find out if Redis is okay.
"""

import asyncio
import os

import aioredis


async def wait_redis():
    """
    Wait until Redis answers to ping(). The function is used to
    check if Redis is okay.
    """
    # os.getenv is used instead of pydantic's settings cause the module
    # is run a stand-alone script
    host = os.getenv('REDIS_HOST', '127.0.0.1')
    redis = await aioredis.create_redis(f'redis://{host}')
    response = await redis.ping()
    while not response:
        await asyncio.sleep(2)
        response = await redis.ping()


if __name__ == '__main__':
    asyncio.run(wait_redis())
