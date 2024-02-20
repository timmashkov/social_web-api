from uuid import UUID

from fastapi import APIRouter, Depends

from models import User
from schemas.user import UserOut, UserIn
from services.users import UserService

users = APIRouter(prefix="/users")

USERS = Depends(UserService)


@users.get("/", response_model=list[UserOut])
async def show_users(user_repo=USERS) -> list[User]:
    return await user_repo.get_users()


@users.get("/{user_id}", response_model=UserOut)
async def show_user(user_id: UUID, user_repo=USERS) -> UserOut:
    return await user_repo.get_user(user_id=user_id)


@users.post("/", response_model=None)
async def post_user(data: UserIn, user_repo=USERS):
    return await user_repo.add_user(data=data)


@users.patch("/{user_id}", response_model=None)
async def patch_user(user_id: UUID, data: UserIn, user_repo=USERS) -> UserOut:
    return await user_repo.change_user(data=data, user_id=user_id)


@users.delete("/{user_id}", response_model=None)
async def delete_user(user_id: UUID, user_repo=USERS) -> dict[str:str]:
    return await user_repo.drop_user(user_id=user_id)
