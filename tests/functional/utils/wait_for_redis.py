"""
This module is used by Docker Compose to find out if Redis is okay.
"""

import asyncio
import logging.config  # noqa: WPS301
import os

import aioredis
import backoff

logging.config.fileConfig(
    fname='tests/functional/log.conf',
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)


def backoff_handler(details):
    """Log backoff processing for Redis."""
    logging.error(
        'Backing off {wait:0.1f} seconds after {tries} tries '
        'calling function {target} with args {args} and kwargs '
        '{kwargs}'.format(**details),
    )


@backoff.on_exception(
    backoff.expo, (ConnectionError,),
    on_backoff=backoff_handler,
    # os.getenv is used instead of pydantic's settings cause the module
    # is run as a stand-alone script:
    max_time=os.getenv('REDIS_CONNECTION_TIMEOUT', '60'),
)
async def wait_redis():
    """
    Wait until Redis answers to ping(). The function is used to
    check if Redis is okay.
    """
    logger.info('Starting to check if Redis is up...')

    # os.getenv is used instead of pydantic's settings cause the module
    # is run as a stand-alone script:
    host = os.getenv('REDIS_HOST', '127.0.0.1')
    redis = await aioredis.create_redis(f'redis://{host}')

    response = await redis.ping()
    attempt = 1
    while not response:
        logger.info(f'Trying to ping Redis (attempt {attempt})...')
        await asyncio.sleep(2)
        response = await redis.ping()
    logger.info('Redis is up...')


if __name__ == '__main__':
    asyncio.run(wait_redis())
