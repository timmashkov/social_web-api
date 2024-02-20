from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator


class UserIn(BaseModel):
    login: str
    password: str
    token: Optional[str] = None
    email: EmailStr
    phone_number: str
    is_verified: Optional[bool] = False

    @field_validator("phone_number")
    def check_phone(cls, data):
        if not data.isdigit() and len(data) != 11:
            raise ValueError(
                "The phone number should be 11 characters in length and be numbers"
            )
        return data


class UserOut(UserIn):
    id: UUID
