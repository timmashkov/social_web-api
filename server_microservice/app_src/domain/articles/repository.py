from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from domain.articles.schema import (
    ArticleIn,
    ArticleOut,
    GetArticleById,
    GetArticleByTitle,
)
from infrastructure.database.models import Article
from infrastructure.database.session import connector


class ArticleRepository:
    def __init__(
        self, session: AsyncSession = Depends(connector.session_local)
    ) -> None:
        self.model = Article
        self.session = session

    async def get_all_articles(self) -> list[Article]:
        stmt = select(self.model).order_by(self.model.id)
        answer = await self.session.execute(stmt)
        result = answer.scalars().all()
        return list(result)

    async def get_article_by_id(self, model_id: GetArticleById) -> ArticleOut | None:
        stmt = select(self.model).where(self.model.id == model_id.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_article_by_title(self, title: GetArticleByTitle) -> ArticleOut | None:
        stmt = select(self.model).where(self.model.title == title.title)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def create_article(self, data: ArticleIn) -> ArticleOut | None:
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(
                self.model.id, self.model.title, self.model.body, self.model.created_at
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_article(
        self, data: ArticleIn, article_id: GetArticleById
    ) -> ArticleOut | None:
        stmt = (
            update(self.model)
            .where(self.model.id == article_id.id)
            .values(**data.model_dump())
            .returning(
                self.model.id, self.model.title, self.model.body, self.model.created_at
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_article(self, article_id: GetArticleById) -> ArticleOut | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == article_id.id)
            .returning(
                self.model.id, self.model.title, self.model.body, self.model.created_at
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
