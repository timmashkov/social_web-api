from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from domain.guests.schema import GetGuestById, GuestOut, GuestIn, GuestUpdate
from infrastructure.database.models import Guest
from infrastructure.database.session import connector


class GuestRepository:
    def __init__(self, session: AsyncSession = Depends(connector.session_local)):
        self.session = session
        self.model = Guest

    async def get_all(self) -> list[Guest]:
        stmt = select(self.model).order_by(self.model.first_name)
        answer = await self.session.execute(stmt)
        result = answer.scalars().all()
        return list(result)

    async def get_guest_by_id(self, cmd: GetGuestById) -> GuestOut | None:
        stmt = select(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def create_guest(self, cmd: GuestIn) -> GuestOut | None:
        stmt = (
            insert(self.model)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.first_name,
                self.model.last_name,
                self.model.event_id,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_guest(
        self, cmd: GuestUpdate, data: GetGuestById
    ) -> GuestOut | None:
        stmt = (
            update(self.model)
            .where(self.model.id == data.id)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.first_name,
                self.model.last_name,
                self.model.event_id,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_guest(self, cmd: GetGuestById) -> GuestOut | None:
        stmt = delete(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
