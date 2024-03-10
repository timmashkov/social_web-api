from domain.guests.repository import GuestRepository
from domain.guests.schema import (
    GetGuestById,
    GuestOut,
    GuestIn,
    GuestUpdate,
    GuestWithTicket,
)

from fastapi import Depends

from infrastructure.cache.redis_handler import CacheRepo
from infrastructure.database.models import Guest

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from infrastructure.exceptions.guests import GuestNotFound, GuestAlreadyExist


class GuestService:
    def __init__(
        self,
        repository: GuestRepository = Depends(GuestRepository),
        cacher: CacheRepo = Depends(CacheRepo),
    ):
        self.repository = repository
        self.cacher = cacher
        self._key = str(self.__class__)

    async def get_all_guest(self) -> list[Guest]:
        answer = await self.repository.get_all()
        await self.cacher.read_cache(self._key)
        return answer

    async def get_guest_by_id(self, cmd: GetGuestById) -> GuestOut:
        answer = await self.repository.get_guest_by_id(cmd=cmd)
        if answer:
            await self.cacher.read_cache(self._key)
            return answer
        raise GuestNotFound

    async def add_guest(self, cmd: GuestIn) -> GuestOut:
        try:
            answer = await self.repository.create_guest(cmd=cmd)
            await self.cacher.create_cache(self._key, cmd)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise GuestAlreadyExist

    async def upd_guest(self, cmd: GuestUpdate, data: GetGuestById) -> GuestOut:
        if await self.get_guest_by_id(cmd=data):
            answer = await self.repository.update_guest(cmd=cmd, data=data)
            await self.cacher.create_cache(self._key, cmd)
            return answer
        raise GuestNotFound

    async def del_guest(self, cmd: GetGuestById) -> GuestOut:
        if await self.get_guest_by_id(cmd=cmd):
            answer = await self.repository.delete_guest(cmd=cmd)
            await self.cacher.delete_cache(self._key)
            return answer
        raise GuestNotFound

    async def get_guest_ticket(self, cmd: GetGuestById) -> GuestWithTicket:
        if await self.get_guest_by_id(cmd=cmd):
            return await self.repository.get_guest_with_ticket(cmd=cmd)
        raise GuestNotFound
