from fastapi import Depends

from domain.tickets.repository import TicketRepository
from domain.tickets.schemas import GetTicketId, TicketOut, TicketIn, TicketUpd
from infrastructure.database.models import Ticket

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from infrastructure.exceptions.tickets import TicketNotFound, TicketAlreadyExist


class TicketService:
    def __init__(self, repository: TicketRepository = Depends(TicketRepository)):
        self.repository = repository

    async def get_all_tickets(self) -> list[Ticket]:
        answer = await self.repository.get_all()
        return answer

    async def get_ticket(self, cmd: GetTicketId) -> TicketOut | None:
        answer = await self.repository.get_ticket_by_id(cmd=cmd)
        if answer:
            return answer
        raise TicketNotFound

    async def create_ticket(self, cmd: TicketIn) -> TicketOut | None:
        try:
            answer = await self.repository.create_ticket(cmd=cmd)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise TicketAlreadyExist

    async def update_ticket(
        self, cmd: TicketUpd, data: GetTicketId
    ) -> TicketOut | None:
        if not await self.get_ticket(cmd=data):
            raise TicketNotFound
        return await self.repository.update_ticket(cmd=cmd, data=data)

    async def delete_ticket(self, cmd: GetTicketId) -> TicketOut | None:
        if not await self.get_ticket(cmd=cmd):
            raise TicketNotFound
        return await self.repository.delete_ticket(cmd=cmd)
