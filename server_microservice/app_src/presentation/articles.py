from uuid import UUID

from fastapi import APIRouter, Depends

from domain.articles.schema import (
    ArticleIn,
    ArticleOut,
    GetArticleById,
    GetArticleByTitle,
)
from services import ArticleService

article_router = APIRouter(prefix="/articles")

art = Depends(ArticleService)


@article_router.get("/", response_model=list[ArticleOut])
async def get_articles(art_repo: ArticleService = art):
    return await art_repo.get_all_articles()


@article_router.get("/by_title/{article_id}", response_model=ArticleOut)
async def get_by_id(article_id: UUID, art_repo: ArticleService = art):
    return await art_repo.get_article_by_id(article_id=GetArticleById(id=article_id))


@article_router.get("/by_id/{article_title}", response_model=ArticleOut)
async def get_by_title(article_title: str, art_repo: ArticleService = art):
    return await art_repo.get_article_by_title(
        title=GetArticleByTitle(title=article_title)
    )


@article_router.post("/register", response_model=ArticleOut)
async def add_article(data: ArticleIn, art_repo: ArticleService = art):
    return await art_repo.create_article(data=data)


@article_router.patch("/upd/{article_id}", response_model=ArticleOut)
async def upd_article(
    article_id: UUID, data: ArticleIn, art_repo: ArticleService = art
):
    return await art_repo.update_article(
        data=data, article_id=GetArticleById(id=article_id)
    )


@article_router.delete("/del/{article_id}", response_model=ArticleOut)
async def del_article(article_id: UUID, art_repo: ArticleService = art):
    return await art_repo.delete_article(article_id=GetArticleById(id=article_id))
