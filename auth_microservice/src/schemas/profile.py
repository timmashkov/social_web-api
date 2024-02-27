from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator, model_validator


class ProfileIn(BaseModel):
    first_name: str
    last_name: str
    age: int
    city: str
    occupation: Optional[str] = None
    bio: Optional[str] = None
    user_id: UUID | str

    @field_validator("age")
    def check_age(cls, data):
        if data < 1:
            raise ValueError("Age must be 1 or higher")
        return data


class ProfileOut(ProfileIn):
    id: UUID


class MatingSchema(BaseModel):
    profile_id: UUID
    friend_id: UUID

    @model_validator(mode="before")
    def check_ids_not_equal(cls, values):
        if values.get("profile_id") == values.get("friend_id"):
            raise ValueError("Profile ID and Friend ID cannot be the same")
        return values


class FriendsOut(ProfileOut):
    friends: list[ProfileOut]
