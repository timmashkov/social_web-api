from utils.handys.cache_helper import redis_connector
from redis import Redis
from fastapi import Depends


class CacheService:
    def __init__(self, cacher: Redis = Depends(redis_connector)):
        self.cacher = cacher
