from datetime import datetime, date
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel, field_validator

__all__ = ("GetEventById", "GetEventByName", "EventUpd", "EventIn", "EventOut")


class GetEventById(BaseModel):
    id: UUID


class GetEventByName(BaseModel):
    name: str


class EventUpd(GetEventByName):
    description: str
    event_date: date


class EventIn(EventUpd): ...


class EventOut(EventIn, GetEventById):
    created_at: datetime
    last_time: float

    @field_validator("last_time")
    def days_count(cls, data):
        return int(data) // 3600
