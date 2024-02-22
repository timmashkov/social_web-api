from uuid import UUID

from fastapi import Depends
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import connector
from models import User
from schemas.auth import UserToken, UserJwtToken, GetUserByLogin


class TokenRepository:
    def __init__(
        self, session: AsyncSession = Depends(connector.scoped_session)
    ) -> None:
        self.session = session
        self.model = User

    async def update_token(self, data: UserJwtToken):
        stmt = (
            update(self.model)
            .where(self.model.id == data.id)
            .values(token=data.token)
            .returning(
                self.model.id,
                self.model.login,
                self.model.email,
                self.model.phone_number,
                self.model.is_verified,
            )
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        answer = result.mappings().first()
        return answer

    async def get_user(self, cmd: GetUserByLogin) -> GetUserByLogin | None:
        stmt = select(
            self.model.id,
            self.model.login,
            self.model.password,
            self.model.email,
        ).where(self.model.login == cmd.login)
        result = await self.session.execute(stmt)
        answer = result.mappings().first()
        return answer

    async def get_token(self, cmd: UUID) -> UserToken | None:
        stmt = select(self.model.token).where(self.model.id == cmd)
        result = await self.session.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer

    async def delete_token(self, cmd: str):
        stmt = (
            update(self.model)
            .where(self.model.id == cmd)
            .values(token="")
            .returning(self.model.id, self.model.token)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        answer = result.mappings().first()
        return answer
