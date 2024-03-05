from uuid import UUID

from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from models import User
from repositories.users import UserRepository
from schemas.user import UserIn, UserOut
from services.auth_handler import AuthHandler
from services.cache_service import CacheService
from utils.exceptions.user_exceptions import UserAlreadyExist, UserNotFound


class UserService:
    """Сервисный репозиторий для юзера"""

    def __init__(
        self,
        user_repo: UserRepository = Depends(UserRepository),
        auth_repo: AuthHandler = Depends(AuthHandler),
        cache_repo: CacheService = Depends(CacheService),
    ) -> None:
        self.user_repo = user_repo
        self.auth_repo = auth_repo
        self.cache_repo = cache_repo

    async def add_user(self, data: UserIn) -> UserOut:
        try:
            salted_pass = self.auth_repo.encode_password(
                password=data.password, salt=data.login
            )
            await self.cache_repo.create_cache(
                "created_user",
                value=UserIn(
                    login=data.login,
                    password=salted_pass,
                    token=data.token,
                    email=data.email,
                    phone_number=data.phone_number,
                    is_verified=data.is_verified,
                ),
            )
            answer = await self.user_repo.create_user(
                data=UserIn(
                    login=data.login,
                    password=salted_pass,
                    token=data.token,
                    email=data.email,
                    phone_number=data.phone_number,
                    is_verified=data.is_verified,
                )
            )
            return answer
        except (UniqueViolationError, IntegrityError):
            raise UserAlreadyExist

    async def get_users(self) -> list[User]:
        answer = await self.user_repo.get_all()
        await self.cache_repo.read_cache("created_user")
        return answer

    async def get_user(self, user_id: UUID) -> UserOut:
        answer = await self.user_repo.get_user_by_id(user_id=user_id)
        if answer:
            await self.cache_repo.read_cache("created_user")
            return answer
        raise UserNotFound

    async def change_user(self, data: UserIn, user_id: UUID) -> UserOut:
        if await self.user_repo.get_user_by_id(user_id=user_id):
            await self.cache_repo.create_cache(
                "created_user",
                value=UserIn(
                    login=data.login,
                    password=data.password,
                    token=data.token,
                    email=data.email,
                    phone_number=data.phone_number,
                    is_verified=data.is_verified,
                ),
            )
            answer = await self.user_repo.update_user(data=data, user_id=user_id)
            return answer
        raise UserNotFound

    async def drop_user(self, user_id: UUID) -> dict[str:str]:
        if await self.user_repo.get_user_by_id(user_id=user_id):
            await self.cache_repo.delete_cache("created_user")
            answer = await self.user_repo.delete_user(user_id=user_id)
            return answer
        raise UserNotFound
