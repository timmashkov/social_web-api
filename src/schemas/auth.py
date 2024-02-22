from uuid import UUID

from pydantic import BaseModel, SecretStr, EmailStr


class UserAccessToken(BaseModel):
    access_token: str


class UserTokens(UserAccessToken):
    refresh_token: str


class UserRefreshToken(UserTokens): ...


class UserToken(BaseModel):
    token: str


class UserId(BaseModel):
    id: UUID


class UserJwtToken(UserId, UserToken):
    id: UUID | str
    token: str = None


class GetUserByLogin(BaseModel):
    login: str
    password: str
