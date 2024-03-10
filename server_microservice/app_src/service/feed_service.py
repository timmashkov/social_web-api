from fastapi import Depends

from domain.articles.repository import ArticleRepository
from domain.events.repository import EventRepository
from domain.guests.repository import GuestRepository
from domain.tickets.repository import TicketRepository
from infrastructure.broker.rabbit_handler import rpc
from infrastructure.cache.redis_handler import CacheRepo


class FeedService:
    def __init__(
        self,
        art_repo: ArticleRepository = Depends(ArticleRepository),
        event_repo: EventRepository = Depends(EventRepository),
        guest_repo: GuestRepository = Depends(GuestRepository),
        tick_repo: TicketRepository = Depends(TicketRepository),
        cacher: CacheRepo = Depends(CacheRepo),
    ):
        self.art_repo = art_repo
        self.eve_repo = event_repo
        self.gue_repo = guest_repo
        self.tic = tick_repo
        self.cacher = cacher
        self._key = str(self.__class__)

    async def get_list_articles(self):
        return await self.art_repo.get_all_articles()

    async def get_list_events(self):
        return await self.eve_repo.get_all()

    async def get_list_guest(self):
        return await self.gue_repo.get_all()

    async def get_list_tick(self):
        return await self.tic.get_all()

    @staticmethod
    async def get_data_from_auth_service():
        """
        RPC method, calls data from another microservice
        :return: result
        """
        result = await rpc.call("rpc_queue")
        return result

    async def make_feed(self) -> dict:
        result = {"Articles": await self.get_list_articles(),
                  "Users and profiles": await self.get_data_from_auth_service(),
                  "Events": await self.get_list_events(),
                  "Guests": await self.get_list_guest(),
                  "Tickets": await self.get_list_tick()}
        await self.cacher.create_cache(self._key, result)
        return result
