from domain.articles.repository import ArticleRepository
from fastapi import Depends

from domain.articles.schema import (
    GetArticleById,
    GetArticleByTitle,
    ArticleOut,
    ArticleIn,
)
from infrastructure.cache.redis_handler import CacheRepo
from infrastructure.database.models import Article


class ArticleService:
    def __init__(
        self,
        repository: ArticleRepository = Depends(ArticleRepository),
        cacher: CacheRepo = Depends(CacheRepo),
    ):
        self.repository = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def get_all_articles(self) -> list[Article]:
        await self.cacher.read_cache(self._key)
        return await self.repository.get_all_articles()

    async def get_article_by_id(self, article_id: GetArticleById) -> ArticleOut:
        await self.cacher.read_cache(self._key)
        return await self.repository.get_article_by_id(model_id=article_id)

    async def get_article_by_title(self, title: GetArticleByTitle):
        await self.cacher.read_cache(self._key)
        return await self.repository.get_article_by_title(title=title)

    async def create_article(self, data: ArticleIn) -> ArticleOut:
        answer = await self.repository.create_article(data=data)
        await self.cacher.create_cache(self._key, data)
        return answer

    async def update_article(
        self, data: ArticleIn, article_id: GetArticleById
    ) -> ArticleOut:
        answer = await self.repository.update_article(data=data, article_id=article_id)
        await self.cacher.create_cache(self._key, data)
        return answer

    async def delete_article(self, article_id: GetArticleById) -> ArticleOut:
        answer = await self.repository.delete_article(article_id=article_id)
        await self.cacher.delete_cache(self._key)
        return answer
