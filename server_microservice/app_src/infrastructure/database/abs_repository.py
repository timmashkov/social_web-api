from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete


class AbstractRepository:
    def __init__(self, model, session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_all(self):
        stmt = select(self.model).order_by(self.model.id)
        answer = await self.session.execute(stmt)
        result = answer.scalars().all()
        return result

    async def get_by_id(self, model_id: UUID):
        stmt = select(self.model).where(self.model.id == model_id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_by_attr(self, attr: str | int | bool | Any):
        stmt = select(self.model).where(getattr(self.model, attr) == attr)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def create(self, data):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update(self, data, model_id: UUID):
        stmt = (
            update(self.model)
            .where(self.model.id == model_id)
            .values(**data.model_dump())
            .returning(self.model)
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete(self, model_id: UUID):
        stmt = delete(self.model).where(self.model.id == model_id).returning(self.model)
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
