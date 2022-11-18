import asyncio
import os

import aioredis


async def wait_redis():
    host = os.getenv("REDIS_HOST", "127.0.0.1")
    redis = await aioredis.create_redis(f'redis://{host}')
    response = await redis.ping()
    while not response:
        await asyncio.sleep(2)
        response = await redis.ping()

if __name__ == "__main__":
    asyncio.run(wait_redis())
