from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel, field_validator, Field

__all__ = ("GetTicketId", "TicketIn", "TicketOut", "TicketUpd")


class TicketExample:
    series = Field(description="series", examples=["1111-1111-1111-1111"])
    exp_date = Field(description="exp_date", examples=["2024-03-10"])


class GetTicketId(BaseModel):
    id: UUID


class TicketUpd(BaseModel):
    series: str = TicketExample.series
    exp_date: date = TicketExample.exp_date
    description: str


class TicketIn(TicketUpd):
    guest_id: UUID

    @field_validator("series")
    def check_series(cls, data):
        if "-" not in data:
            raise ValueError("Wrong series format")
        if len(data.split("-")) != 4 and not all(
            map(lambda x: len(x) == 4, data.split("-"))
        ):
            raise ValueError("Not enough numbers")
        return data


class TicketOut(TicketIn, GetTicketId):
    created_at: datetime
    last_time: float | str

    @field_validator("last_time")
    def days_count(cls, data):
        return f"{int(float(data)) // 3600} days"
