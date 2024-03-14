import pickle

from configuration.core.config import base_config
from redis import asyncio as aioredis


class CacheService:
    def __init__(self):
        self.redis_pool = aioredis.ConnectionPool.from_url(
            f"redis://{base_config.REDIS_HOST}:{base_config.REDIS_PORT}/0"
        )
        self.cacher = aioredis.Redis(connection_pool=self.redis_pool)

    async def create_cache(self, key, value):
        await self.cacher.set(key, pickle.dumps(value), ex=base_config.EXPIRATION)

    async def read_cache(self, key):
        return await self.cacher.get(key)

    async def update_cache(self, key, value):
        await self.cacher.set(key, pickle.dumps(value), ex=base_config.EXPIRATION)

    async def delete_cache(self, key):
        await self.cacher.delete(key)

    async def close_connections(self):
        await self.cacher.aclose()
        await self.redis_pool.disconnect()
