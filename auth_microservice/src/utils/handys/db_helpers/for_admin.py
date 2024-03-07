from uuid import UUID

from sqlalchemy import select, update

from configuration.core.database import connector
from models import User
from schemas.auth import GetUserByLogin, UserJwtToken, UserToken


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
