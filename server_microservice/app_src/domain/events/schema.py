from datetime import datetime, date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

__all__ = ("GetEventById", "GetEventByName", "EventUpd", "EventIn", "EventOut")


class GetEventById(BaseModel):
    id: UUID


class GetEventByName(BaseModel):
    name: str


class EventUpd(GetEventByName):
    description: str
    event_date: date


class EventIn(EventUpd): ...


class EventOut(EventIn):
    created_at: datetime
    last_time: Optional[datetime] = str
