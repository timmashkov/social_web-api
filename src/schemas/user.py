from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator, SecretStr


class UserIn(BaseModel):
    first_name: str
    last_name: str
    password: Optional[str] = None
    age: int
    city: str
    email: EmailStr
    token: Optional[str] = None
    phone_number: str
    occupation: Optional[str] = None
    bio: Optional[str] = None

    @field_validator("phone_number")
    def check_phone(cls, data):
        if not data.isdigit() and len(data) != 11:
            raise ValueError(
                "The phone number should be 11 characters in length and be numbers"
            )
        return data


class UserOut(UserIn):
    id: UUID
