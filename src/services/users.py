from uuid import UUID

from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from models import User
from repositories.users import UserRepository
from schemas.user import UserIn, UserOut
from utils.exceptions.user_exceptions import UserAlreadyExist, UserNotFound


class UserService:
    def __init__(self, user_repo: UserRepository = Depends(UserRepository)) -> None:
        self.user_repo = user_repo

    async def add_user(self, data: UserIn) -> UserOut:
        try:
            answer = await self.user_repo.create_user(data=data)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise UserAlreadyExist

    async def get_users(self) -> list[User]:
        answer = await self.user_repo.get_all()
        return answer

    async def get_user(self, user_id: UUID) -> UserOut:
        answer = await self.user_repo.get_user_by_id(user_id=user_id)
        if answer:
            return answer
        raise UserNotFound

    async def change_user(self, data: UserIn, user_id: UUID) -> UserOut:
        if await self.user_repo.get_user_by_id(user_id=user_id):
            answer = await self.user_repo.update_user(data=data, user_id=user_id)
            return answer
        raise UserNotFound

    async def drop_user(self, user_id: UUID) -> dict[str:str]:
        if await self.user_repo.get_user_by_id(user_id=user_id):
            answer = await self.user_repo.delete_user(user_id=user_id)
            return answer
        raise UserNotFound
