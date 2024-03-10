from domain.articles.repository import ArticleRepository
from fastapi import Depends

from infrastructure.broker.rabbit_handler import mq, rpc
from infrastructure.cache.redis_handler import CacheRepo


class FeedService:
    def __init__(
        self,
        repository: ArticleRepository = Depends(ArticleRepository),
        cacher: CacheRepo = Depends(CacheRepo),
    ):
        self.art_repo = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def get_list_articles(self):
        await self.cacher.read_cache(self._key)
        return await self.art_repo.get_all_articles()

    async def get_rpc_list_profiles(self):
        result = await rpc.call("rpc_queue")
        return result

    async def make_feed(self) -> list:
        data = [*await self.get_list_articles(), *await self.get_rpc_list_profiles()]
        await self.cacher.create_cache(self._key, data)
        return data
