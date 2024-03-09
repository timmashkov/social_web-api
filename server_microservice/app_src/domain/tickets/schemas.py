from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel, field_validator, Field

__all__ = ("GetTicketId", "TicketIn", "TicketOut")


class TicketExample:
    series = Field(description="series", examples=["1111-1111-1111-1111"])


class GetTicketId(BaseModel):
    id: UUID


class TicketIn(BaseModel):
    series: str = TicketExample.series
    description: str

    @field_validator("series")
    def check_series(cls, data):
        if "-" not in data:
            raise ValueError("Wrong series format")
        if len(data.split()) != 4 and not all(map(lambda x: len(x) == 4, data)):
            raise ValueError("Not enough numbers")
        return data


class TicketOut(TicketIn, GetTicketId):
    created_at: datetime
    exp_date: date
    last_time: float

    @field_validator("last_time")
    def days_count(cls, data):
        return f"{int(data) // 3600} days"
