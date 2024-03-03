from fastapi import APIRouter
from .articles import article_router


main_router = APIRouter(prefix="/main")


main_router.include_router(router=article_router, tags=["Articles"])
