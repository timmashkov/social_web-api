from fastapi import Depends

from repositories.token import TokenRepository
from schemas.auth import GetUserById, CreateJwtToken
from services.auth_handler import AuthHandler
from utils.exceptions.user_exceptions import UserNotFound, WrongPassword

auth = AuthHandler()


class AuthService:
    def __init__(self, repository: TokenRepository = Depends(TokenRepository)):
        self.repository = repository

    async def login(self, data: GetUserById):
        user = await self.repository.get_user(cmd=data)
        if not user:
            raise UserNotFound
        if not auth.verify_password(data.password,
                                    data.login,
                                    user.password):
            raise WrongPassword
        access_token = auth.encode_token(user.id)
        refresh_token = auth.encode_refresh_token(user.id)
        try:
            await self.repository.update_token(data=CreateJwtToken(id=user.id, token=refresh_token))
        except Exception as e:
            return {"error": e}
        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token}
        return tokens
