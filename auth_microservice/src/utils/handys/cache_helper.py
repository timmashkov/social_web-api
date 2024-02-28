from redis import asyncio as aioredis
from redis import Redis

from configuration.core.config import base_config


def redis_maker() -> aioredis.ConnectionPool:
    return aioredis.ConnectionPool.from_url(
        f"redis://{base_config.REDIS_HOST}:{base_config.REDIS_PORT}"
    )


redis_pool = redis_maker()


def redis_connector() -> Redis:
    return Redis(connection_pool=redis_pool)
