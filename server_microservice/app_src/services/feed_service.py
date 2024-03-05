from domain.articles.repository import ArticleRepository
from fastapi import Depends

from infrastructure.broker.rabbit_handler import mq
from infrastructure.utils import get_msg


class FeedService:
    def __init__(self, repository: ArticleRepository = Depends(ArticleRepository)):
        self.art_repo = repository

    async def get_list_articles(self):
        return await self.art_repo.get_all_articles()

    async def get_list_profiles(self):
        return get_msg

    async def make_feed(self) -> list:
        data = [await self.get_list_articles(), await self.get_list_profiles()]
        return data
