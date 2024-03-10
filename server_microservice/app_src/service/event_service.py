from domain.events.repository import EventRepository
from domain.events.schema import (
    GetEventById,
    EventOut,
    GetEventByName,
    EventIn,
    EventUpd,
    FullEventData,
)

from fastapi import Depends

from infrastructure.database.models import Event
from infrastructure.exceptions.events import EventNotFound, EventAlreadyExist

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError


class EventService:
    def __init__(self, repository: EventRepository = Depends(EventRepository)):
        self.repository = repository

    async def get_all_events(self) -> list[Event]:
        answer = await self.repository.get_all()
        return answer

    async def get_event_by_id(self, cmd: GetEventById) -> EventOut:
        answer = await self.repository.get_event_by_id(cmd=cmd)
        if not answer:
            raise EventNotFound
        return answer

    async def get_event_by_name(self, cmd: GetEventByName) -> EventOut:
        answer = await self.repository.get_event_by_name(cmd=cmd)
        if not answer:
            raise EventNotFound
        return answer

    async def initiate_event(self, cmd: EventIn) -> EventOut:
        try:
            answer = await self.repository.create_event(cmd=cmd)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise EventAlreadyExist

    async def change_event(self, cmd: EventUpd, data: GetEventById) -> EventOut:
        if await self.get_event_by_id(cmd=data):
            return await self.repository.update_event(data=cmd, cmd=data)
        raise EventNotFound

    async def delete_event(self, cmd: GetEventById) -> EventOut:
        if await self.get_event_by_id(cmd=cmd):
            return await self.repository.delete_event(cmd=cmd)
        raise EventNotFound

    async def get_full_event(self, cmd: GetEventById) -> FullEventData:
        if await self.get_event_by_id(cmd=cmd):
            return await self.repository.get_full_event(cmd=cmd)
        raise EventNotFound
