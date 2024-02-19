from uuid import UUID

from fastapi import Depends

from models import User
from repositories.users import UserRepository
from schemas.user import UserIn, UserOut


class UserService:
    def __init__(self, user_repo: UserRepository = Depends(UserRepository)) -> None:
        self.user_repo = user_repo

    async def add_user(self, data: UserIn) -> UserOut:
        answer = await self.user_repo.create_user(data=data)
        return answer

    async def get_users(self) -> list[User]:
        answer = await self.user_repo.get_all()
        return answer

    async def get_user(self, user_id: UUID) -> UserOut:
        answer = await self.user_repo.get_user_by_id(user_id=user_id)
        return answer

    async def change_user(self, data: UserIn, user_id: UUID) -> UserOut:
        answer = await self.user_repo.update_user(data=data, user_id=user_id)
        return answer

    async def drop_user(self, user_id: UUID) -> dict[str: str]:
        answer = await self.user_repo.delete_user(user_id=user_id)
        return answer
    