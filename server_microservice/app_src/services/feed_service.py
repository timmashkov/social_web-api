from domain.articles.repository import ArticleRepository
from fastapi import Depends

from infrastructure.broker.rabbit_handler import mq


class FeedService:
    def __init__(self, repository: ArticleRepository = Depends(ArticleRepository)):
        self.art_repo = repository

    async def get_list_articles(self):
        return await self.art_repo.get_all_articles()

    async def get_list_profiles(self):
        await mq.mq_connect()
        result = await mq.get_message("sw-feed")
        await mq.mq_close_conn()
        return result

    async def make_feed(self) -> list:
        data = [*await self.get_list_articles(), *await self.get_list_profiles()]
        return data
