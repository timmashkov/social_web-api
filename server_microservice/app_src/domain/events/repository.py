from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from domain.events.schema import (
    GetEventById,
    EventOut,
    GetEventByName,
    EventIn,
    EventUpd,
)
from infrastructure.database.models import Event
from infrastructure.database.session import connector


class EventRepository:
    def __init__(
        self, session: AsyncSession = Depends(connector.session_local)
    ) -> None:
        self.model = Event
        self.session = session

    async def get_all(self) -> list[Event]:
        stmt = select(self.model).order_by(self.model.name)
        answer = await self.session.execute(stmt)
        result = answer.scalars().all()
        return list(result)

    async def get_event_by_id(self, cmd: GetEventById) -> EventOut | None:
        stmt = select(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_event_by_name(self, cmd: GetEventByName) -> EventOut | None:
        stmt = select(self.model).where(self.model.name == cmd.name)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def create_event(self, cmd: EventIn) -> EventOut | None:
        stmt = (
            insert(self.model)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.name,
                self.model.description,
                self.model.event_date,
                self.model.created_at,
                self.model.last_time,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_event(self, data: EventUpd, cmd: GetEventById) -> EventOut | None:
        stmt = (
            update(self.model)
            .where(self.model.id == cmd.id)
            .values(**data.model_dump())
            .returning(
                self.model.id,
                self.model.name,
                self.model.description,
                self.model.event_date,
                self.model.created_at,
                self.model.last_time,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_event(self, cmd: GetEventById) -> EventOut | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == cmd.id)
            .returning(
                self.model.id,
                self.model.name,
                self.model.description,
                self.model.event_date,
                self.model.created_at,
                self.model.last_time,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
