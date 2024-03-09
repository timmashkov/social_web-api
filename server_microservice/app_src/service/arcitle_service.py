from domain.articles.repository import ArticleRepository
from fastapi import Depends

from domain.articles.schema import (
    GetArticleById,
    GetArticleByTitle,
    ArticleOut,
    ArticleIn,
)
from infrastructure.database.models import Article


class ArticleService:
    def __init__(self, repository: ArticleRepository = Depends(ArticleRepository)):
        self.repository = repository

    async def get_all_articles(self) -> list[Article]:
        return await self.repository.get_all_articles()

    async def get_article_by_id(self, article_id: GetArticleById) -> ArticleOut:
        return await self.repository.get_article_by_id(model_id=article_id)

    async def get_article_by_title(self, title: GetArticleByTitle):
        return await self.repository.get_article_by_title(title=title)

    async def create_article(self, data: ArticleIn) -> ArticleOut:
        return await self.repository.create_article(data=data)

    async def update_article(
        self, data: ArticleIn, article_id: GetArticleById
    ) -> ArticleOut:
        return await self.repository.update_article(data=data, article_id=article_id)

    async def delete_article(self, article_id: GetArticleById) -> ArticleOut:
        return await self.repository.delete_article(article_id=article_id)
