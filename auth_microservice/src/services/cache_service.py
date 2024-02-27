from utils.handys.cache_helper import redis_connector


class CacheService:
    def __init__(self):
        self.cacher = redis_connector()


