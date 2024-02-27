from typing import Any
from uuid import UUID

from sqlalchemy import select, update

from configuration.core.database import connector
from models import User
from schemas.auth import GetUserByLogin, UserJwtToken, UserId, UserToken
from services.auth_handler import AuthHandler
from utils.exceptions.auth_exceptions import Unauthorized
from utils.exceptions.user_exceptions import UserNotFound, WrongPassword

"""
Вспомогательные фичи для админки, для игзбегания DI
"""

auth = AuthHandler()


async def find_user(data: GetUserByLogin) -> GetUserByLogin | None:
    """Поиск юзера"""
    async with connector.engine.connect() as session:
        stmt = select(
            User.id,
            User.login,
            User.password,
            User.email,
        ).where(User.login == data.login)
        result = await session.execute(stmt)
        answer = result.mappings().first()
        return answer


async def change_token(data: UserJwtToken):
    """Смена токена"""
    async with connector.engine.connect() as session:
        stmt = (
            update(User)
            .where(User.id == data.id)
            .values(token=data.token)
            .returning(
                User.id,
                User.login,
                User.email,
                User.phone_number,
                User.is_verified,
            )
        )
        result = await session.execute(stmt)
        await session.commit()
        answer = result.mappings().first()
        return answer


async def find_token(cmd: UUID) -> UserToken | None:
    """Поиск токена"""
    async with connector.engine.connect() as session:
        stmt = select(User.token).where(User.id == cmd)
        result = await session.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer


async def verify_user(cmd: GetUserByLogin) -> dict[str, str] | dict[str, Any]:
    """подтверждение юзера"""
    user = await find_user(data=cmd)
    if not user:
        raise UserNotFound
    if not auth.verify_password(cmd.password, cmd.login, user.password):
        raise WrongPassword
    access_token = auth.encode_token(user.id)
    refresh_token = auth.encode_refresh_token(user.id)
    try:
        await change_token(data=UserJwtToken(id=user.id, token=refresh_token))
    except Exception as e:
        return {"error": e}
    tokens = {"access_token": access_token, "refresh_token": refresh_token}
    return tokens


async def check_auth(refresh_token) -> UserId:
    """Подтверджение аутентификации"""
    user_id = auth.decode_token(refresh_token)
    exist_token = await find_token(cmd=user_id[1:-1])
    if not exist_token:
        raise Unauthorized
    try:
        if exist_token == refresh_token:
            return UserId(id=user_id)
        else:
            raise Unauthorized
    except AttributeError:
        raise Unauthorized
