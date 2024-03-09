from domain.guests.repository import GuestRepository
from domain.guests.schema import GetGuestById, GuestOut, GuestIn, GuestUpdate

from fastapi import Depends

from infrastructure.database.models import Guest

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from infrastructure.exceptions.guests import GuestNotFound, GuestAlreadyExist


class GuestService:
    def __init__(self, repository: GuestRepository = Depends(GuestRepository)):
        self.repository = repository

    async def get_all_guest(self) -> list[Guest]:
        answer = await self.repository.get_all()
        return answer

    async def get_guest_by_id(self, cmd: GetGuestById) -> GuestOut:
        answer = await self.repository.get_guest_by_id(cmd=cmd)
        if answer:
            return answer
        raise GuestNotFound

    async def add_guest(self, cmd: GuestIn) -> GuestOut:
        try:
            answer = await self.repository.create_guest(cmd=cmd)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise GuestAlreadyExist

    async def upd_guest(self, cmd: GuestUpdate, data: GetGuestById) -> GuestOut:
        if await self.get_guest_by_id(cmd=data):
            answer = await self.repository.update_guest(cmd=cmd, data=data)
            return answer
        raise GuestNotFound

    async def del_guest(self, cmd: GetGuestById) -> GuestOut:
        if not await self.get_guest_by_id(cmd=cmd):
            answer = await self.repository.delete_guest(cmd=cmd)
            return answer
        raise GuestNotFound
