from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

__all__ = ("GetArticleById", "GetArticleByTitle", "ArticleIn", "ArticleOut")


class GetArticleById(BaseModel):
    id: UUID | str


class GetArticleByTitle(BaseModel):
    title: str


class ArticleIn(GetArticleByTitle):
    body: str


class ArticleOut(GetArticleById, ArticleIn):
    created_at: datetime | str
