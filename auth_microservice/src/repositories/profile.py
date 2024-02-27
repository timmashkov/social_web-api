from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from configuration.core.database import connector
from models import Profile
from schemas.profile import ProfileOut, ProfileIn, MatingSchema, FriendsOut


class ProfileRepository:
    def __init__(self, session: AsyncSession = Depends(connector.scoped_session)):
        self.session = session
        self.model = Profile

    async def get_all(self) -> list[Profile]:
        stmt = select(self.model).order_by(self.model.id)
        answer = await self.session.execute(stmt)
        result = answer.scalars().all()
        return list(result)

    async def get_profile_by_id(self, profile_id: UUID) -> ProfileOut | None:
        stmt = select(self.model).where(self.model.id == profile_id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_profile_by_name(self, name: str):
        stmt = select(self.model).where(self.model.first_name == name)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def create_profile(self, data: ProfileIn) -> ProfileOut | None:
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(
                self.model.id,
                self.model.first_name,
                self.model.last_name,
                self.model.age,
                self.model.city,
                self.model.occupation,
                self.model.bio,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_profile(
        self, data: ProfileIn, profile_id: UUID
    ) -> ProfileOut | None:
        stmt = (
            update(self.model)
            .where(self.model.id == profile_id)
            .values(**data.model_dump())
            .returning(
                self.model.id,
                self.model.first_name,
                self.model.last_name,
                self.model.age,
                self.model.city,
                self.model.occupation,
                self.model.bio,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_profile(self, profile_id: UUID) -> dict[str:str]:
        stmt = delete(self.model).where(self.model.id == profile_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return {"message": f"Profile №{profile_id} has been deleted"}

    async def add_friends(self, friend_in: MatingSchema, friend_new: MatingSchema):
        query_profile = (
            select(self.model)
            .options(joinedload(self.model.friends))
            .where(self.model.id == friend_in.id)
        )
        query_friend = select(self.model).where(self.model.id == friend_new.id)
        answer_profile = await self.session.execute(query_profile)
        answer_friend = await self.session.execute(query_friend)
        profile = answer_profile.scalars().first()
        friend = answer_friend.scalars().first()
        profile.friends.append(friend)
        await self.session.commit()
        return {"message": f"Friend {friend} added successfully"}

    async def get_profile_with_friends(self, profile_id: UUID) -> FriendsOut | None:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.friends))
            .where(self.model.id == profile_id)
        )
        answer = await self.session.execute(stmt)
        result = answer.unique().scalar_one_or_none()
        return result
