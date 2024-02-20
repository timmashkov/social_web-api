from fastapi import Depends

from repositories.token import TokenRepository
from schemas.auth import GetUserById
from services.auth_handler import AuthHandler
from utils.exceptions.user_exceptions import UserNotFound

auth = AuthHandler()


class AuthService:
    def __init__(self, repository: TokenRepository = Depends(TokenRepository)):
        self.repository = repository

    async def login(self, data: GetUserById):
        answer = await self.repository.get_user(cmd=data)
        if not answer:
            raise UserNotFound
