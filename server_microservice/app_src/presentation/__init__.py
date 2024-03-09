from fastapi import APIRouter
from .articles import article_router
from .feed import feed_router
from .events import event_router


main_router = APIRouter(prefix="/main")


main_router.include_router(router=article_router, tags=["Articles"])
main_router.include_router(router=feed_router, tags=["Feed"])
main_router.include_router(router=event_router, tags=["Events"])
