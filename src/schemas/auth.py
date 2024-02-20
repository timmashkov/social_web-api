from uuid import UUID

from pydantic import BaseModel, SecretStr, EmailStr


class UserAccessToken(BaseModel):
    access_token: SecretStr


class UserTokens(UserAccessToken):
    refresh_token: SecretStr


class UserRefreshToken(UserTokens): ...


class CreateJwtToken(BaseModel):
    id: UUID
    token: SecretStr


class DeleteJwtToken(BaseModel):
    id: UUID
    token: SecretStr = None


class GetUserById(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    password: SecretStr
    email: EmailStr
