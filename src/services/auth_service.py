from typing import Any

from fastapi import Depends

from repositories.token import TokenRepository
from schemas.auth import (
    UserId,
    UserRefreshToken, UserJwtToken, GetUserByLogin,
)
from services.auth_handler import AuthHandler
from utils.exceptions.auth_exceptions import Unauthorized
from utils.exceptions.user_exceptions import UserNotFound, WrongPassword

auth = AuthHandler()


class AuthService:
    def __init__(self, repository: TokenRepository = Depends(TokenRepository)) -> None:
        self.repository = repository

    async def login(self, data: GetUserByLogin) -> dict[str, str] | dict[str, Any]:
        user = await self.repository.get_user(cmd=data)
        if not user:
            raise UserNotFound
        if not auth.verify_password(data.password, data.login, user.password):
            raise WrongPassword
        access_token = auth.encode_token(user.id)
        refresh_token = auth.encode_refresh_token(user.id)
        try:
            await self.repository.update_token(
                data=UserJwtToken(id=user.id, token=refresh_token)
            )
        except Exception as e:
            return {"error": e}
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens

    async def logout(self, refresh_token):
        user_id = auth.decode_refresh_token(refresh_token)
        token = await self.repository.get_token(cmd=user_id[1:-1])
        if not token:
            raise Unauthorized
        if token == refresh_token:
            result = await self.repository.delete_token(
                cmd=user_id[1:-1])
            return result
        raise Unauthorized

    async def is_auth(self, refresh_token):
        user_id = auth.decode_token(refresh_token)
        exist_token = await self.repository.get_token(cmd=user_id)
        if not exist_token:
            raise Unauthorized
        try:
            token = exist_token.tokens.get_secret_value()
            if token == refresh_token:
                return UserId(id=user_id)
            else:
                raise Unauthorized
        except AttributeError:
            raise Unauthorized

    async def refresh_token(self, refresh_token):
        user_id = auth.decode_refresh_token(refresh_token)
        exist_token = await self.repository.get_token(cmd=user_id[1:-1])
        if not exist_token:
            raise Unauthorized
        else:
            if exist_token == refresh_token:
                new_token = auth.refresh_token(refresh_token=refresh_token)
                print(new_token)
                await self.repository.update_token(
                    data=UserJwtToken(id=user_id[1:-1], token=new_token.access_token)
                )

                return UserRefreshToken(
                    access_token=new_token.access_token,
                    refresh_token=new_token.refresh_token,
                )
            else:
                raise Unauthorized
