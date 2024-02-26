from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator


class ProfileIn(BaseModel):
    first_name: str
    last_name: str
    age: int
    city: str
    occupation: Optional[str] = None
    bio: Optional[str] = None

    @field_validator("age")
    def check_age(cls, data):
        if data < 1:
            raise ValueError("Age must be 1 or higher")
        return data


class ProfileOut(ProfileIn):
    id: UUID
