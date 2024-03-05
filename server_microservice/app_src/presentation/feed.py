from fastapi import APIRouter, Depends

from services import FeedService

feed_router = APIRouter(prefix="/feed")

FEED = Depends(FeedService)


@feed_router.get("/", response_model=None)
async def show_feed(feed_repo: FeedService = FEED):
    return await feed_repo.make_feed()
