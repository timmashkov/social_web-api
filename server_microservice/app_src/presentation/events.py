from uuid import UUID

from fastapi import APIRouter, Depends

from domain.events.schema import (
    EventOut,
    GetEventById,
    GetEventByName,
    EventIn,
    EventUpd,
)
from infrastructure.database.models import Event
from service import EventService

event_router = APIRouter(prefix="/event")


@event_router.get("/", response_model=list[EventOut])
async def show_events(event_repo: EventService = Depends(EventService)) -> list[Event]:
    return await event_repo.get_all_events()


@event_router.get("/{event_id}", response_model=EventOut)
async def show_event_by_id(
    event_id: UUID, event_repo: EventService = Depends(EventService)
) -> EventOut:
    return await event_repo.get_event_by_id(cmd=GetEventById(id=event_id))


@event_router.get("/{event_name}", response_model=EventOut)
async def show_event_by_id(
    event_name: str, event_repo: EventService = Depends(EventService)
) -> EventOut:
    return await event_repo.get_event_by_name(cmd=GetEventByName(name=event_name))


@event_router.post("/initial", response_model=EventOut)
async def make_event(
    cmd: EventIn, event_repo: EventService = Depends(EventService)
) -> EventOut:
    return await event_repo.initiate_event(cmd=cmd)


@event_router.patch("/upd/{event_id}", response_model=EventOut)
async def make_event(
    cmd: EventUpd, event_id: UUID, event_repo: EventService = Depends(EventService)
) -> EventOut:
    return await event_repo.change_event(cmd=cmd, data=GetEventById(id=event_id))


@event_router.delete("/del/{event_id}", response_model=EventOut)
async def make_event(
    event_id: UUID, event_repo: EventService = Depends(EventService)
) -> EventOut:
    return await event_repo.delete_event(cmd=GetEventById(id=event_id))
