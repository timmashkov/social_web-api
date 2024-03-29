from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from configuration.core.database import connector
from models import User
from schemas.user import UserOut, UserIn


class UserRepository:
    """Репозиторий с крудами для юзера"""

    def __init__(
        self, session: AsyncSession = Depends(connector.scoped_session)
    ) -> None:
        self.session = session
        self.model = User

    async def get_all(self) -> list[User]:
        stmt = select(self.model).order_by(self.model.id)
        answer = await self.session.execute(stmt)
        result = answer.scalars().all()
        return list(result)

    async def get_user_by_id(self, user_id: UUID) -> UserOut | None:
        stmt = select(self.model).where(self.model.id == user_id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def create_user(self, data: UserIn) -> UserOut | None:
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(
                self.model.id,
                self.model.login,
                self.model.email,
                self.model.phone_number,
                self.model.registered_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_user(self, data: UserIn, user_id: UUID) -> UserOut | None:
        stmt = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(**data.model_dump())
            .returning(
                self.model.id,
                self.model.login,
                self.model.email,
                self.model.phone_number,
                self.model.registered_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_user(self, user_id: UUID) -> dict[str:str]:
        stmt = delete(self.model).where(self.model.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return {"message": f"User №{user_id} has been deleted"}
