from fastapi import Depends
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import connector
from models import User
from schemas.auth import CreateJwtToken, GetUserById, DeleteJwtToken


class TokenRepository:
    def __init__(
        self, session: AsyncSession = Depends(connector.scoped_session)
    ) -> None:
        self.session = session
        self.model = User

    async def update_token(self, data: CreateJwtToken):
        stmt = (
            update(self.model)
            .where(self.model.id == data.id)
            .values(token=data.token)
            .returning(
                self.model.id,
                self.model.first_name,
                self.model.last_name,
                self.model.age,
                self.model.city,
                self.model.email,
                self.model.phone_number,
                self.model.occupation,
                self.model.bio,
            )
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        answer = result.mappings().first()
        return answer

    async def get_user(self, cmd: GetUserById) -> GetUserById | None:
        stmt = select(
            self.model.id,
            self.model.first_name,
            self.model.last_name,
            self.model.password,
            self.model.email,
        ).where(self.model.id == cmd.id)
        result = await self.session.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer

    async def get_tokens(self, cmd: GetUserById) -> GetUserById | None:
        stmt = select(self.model.token).where(self.model.id == cmd.id)
        result = await self.session.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer

    async def delete_token(self, cmd: DeleteJwtToken):
        stmt = (
            update(self.model.token)
            .where(self.model.id == cmd.id)
            .values(token=cmd.token)
            .returning(self.model.id, self.model.token)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        answer = result.mappings().first()
        return answer
