from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from domain.tickets.schemas import GetTicketId, TicketOut, TicketIn, TicketUpd
from infrastructure.database.models import Ticket
from infrastructure.database.session import connector


class TicketRepository:
    def __init__(
        self, session: AsyncSession = Depends(connector.session_local)
    ) -> None:
        self.session = session
        self.model = Ticket

    async def get_all(self) -> list[Ticket]:
        stmt = select(self.model).order_by(self.model.id)
        answer = await self.session.execute(stmt)
        result = answer.scalars().all()
        return list(result)

    async def get_ticket_by_id(self, cmd: GetTicketId) -> TicketOut | None:
        stmt = select(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.mappings().first()
        return result

    async def create_ticket(self, cmd: TicketIn) -> TicketOut | None:
        stmt = (
            insert(self.model)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.series,
                self.model.description,
                self.model.created_at,
                self.model.exp_date,
                self.model.last_time,
                self.model.guest_id,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_ticket(
        self, cmd: TicketUpd, data: GetTicketId
    ) -> TicketOut | None:
        stmt = (
            update(self.model)
            .where(self.model.id == data.id)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.series,
                self.model.description,
                self.model.created_at,
                self.model.exp_date,
                self.model.last_time,
                self.model.guest_id,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_ticket(self, cmd: GetTicketId) -> TicketOut | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == cmd.id)
            .returning(
                self.model.id,
                self.model.series,
                self.model.description,
                self.model.created_at,
                self.model.exp_date,
                self.model.last_time,
                self.model.guest_id,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
