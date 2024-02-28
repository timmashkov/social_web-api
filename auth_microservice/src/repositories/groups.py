from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from fastapi import Depends

from configuration.core.database import connector
from models import Group
from schemas.group import (
    GroupOut,
    GroupSearchById,
    GroupSearchByTitle,
    GroupIn,
    GroupUpdateIn,
)


class GroupRepository:
    def __init__(self, session: AsyncSession = Depends(connector)):
        self.session = session
        self.model = Group

    async def get_all(self) -> list[Group]:
        stmt = select(self.model).order_by(self.model.created_at)
        answer = await self.session.execute(stmt)
        result = answer.scalars().all()
        return list(result)

    async def get_group_by_id(self, cmd: GroupSearchById) -> GroupOut | None:
        stmt = select(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_group_by_title(self, cmd: GroupSearchByTitle) -> GroupOut | None:
        stmt = select(self.model).where(self.model.title == cmd.title)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def create_group(self, cmd: GroupIn) -> GroupOut | None:
        stmt = (
            insert(self.model)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.title,
                self.model.description,
                self.model.group_admin,
                self.model.is_official,
                self.model.created_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_group(self, cmd: GroupUpdateIn) -> GroupOut | None:
        stmt = (
            update(self.model)
            .where(self.model.id == cmd.id)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.title,
                self.model.description,
                self.model.group_admin,
                self.model.is_official,
                self.model.created_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_group(self, cmd: GroupSearchById) -> GroupOut | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == cmd.id)
            .returning(
                self.model.id,
                self.model.title,
                self.model.description,
                self.model.group_admin,
                self.model.is_official,
                self.model.created_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
