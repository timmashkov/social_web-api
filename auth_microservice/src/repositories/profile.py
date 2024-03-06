from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from configuration.core.database import connector
from models import Profile, ProfilePost
from schemas.profile import (
    ProfileOut,
    ProfileIn,
    MatingSchema,
    FriendsOut,
    ProfileUpdateIn,
    ProfilePostIn,
    ProfilePostOut,
    GetProfilePostById,
    GetProfilePostByTitle,
)


class ProfileRepository:
    """Репозиторий с крудами для профиля"""

    def __init__(self, session: AsyncSession = Depends(connector.scoped_session)):
        self.session = session
        self.model = Profile
        self.model_post = ProfilePost

    async def get_all(self) -> list[Profile]:
        stmt = select(self.model).order_by(self.model.id)
        answer = await self.session.execute(stmt)
        result = answer.scalars().all()
        return list(result)

    async def get_all_for_mq(self):
        stmt = select(self.model).order_by(self.model.id)
        answer = await self.session.execute(stmt)
        result = answer.scalars().all()
        return list(result)

    async def get_profile_by_id(self, profile_id: UUID) -> ProfileOut | None:
        stmt = select(self.model).where(self.model.id == profile_id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_profile_post_by_id(
        self, post_id: GetProfilePostById
    ) -> ProfilePostOut | None:
        stmt = select(self.model_post).where(self.model_post.id == post_id.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_profile_post_by_title(
        self, post_title: GetProfilePostByTitle
    ) -> ProfilePostOut | None:
        stmt = select(self.model_post).where(self.model_post.title == post_title.title)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_profile_by_name(self, name: str) -> ProfileOut | None:
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
                self.model.created_at,
                self.model.user_id,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def create_profile_post(self, data: ProfilePostIn) -> ProfilePostOut | None:
        stmt = (
            insert(self.model_post)
            .values(**data.model_dump())
            .returning(
                self.model_post.id,
                self.model_post.title,
                self.model_post.hashtag,
                self.model_post.text,
                self.model_post.post_author,
                self.model_post.written_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_profile_post(
        self, data: ProfilePostIn, post_id: GetProfilePostById
    ) -> ProfilePostOut | None:
        stmt = (
            update(self.model_post)
            .where(self.model_post.id == post_id.id)
            .values(**data.model_dump())
            .returning(
                self.model_post.id,
                self.model_post.title,
                self.model_post.hashtag,
                self.model_post.text,
                self.model_post.post_author,
                self.model_post.written_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_profile(
        self, data: ProfileUpdateIn, profile_id: UUID
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
                self.model.created_at,
                self.model.user_id,
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

    async def delete_profile_post(self, post_id: GetProfilePostById) -> dict[str:str]:
        stmt = delete(self.model_post).where(self.model_post.id == post_id.id)
        await self.session.execute(stmt)
        await self.session.commit()
        return {"message": f"Post of Profile №{post_id} has been deleted"}

    async def add_friends(self, cmd: MatingSchema) -> dict[str:str]:
        query_profile = (
            select(self.model)
            .options(joinedload(self.model.friends))
            .where(self.model.id == cmd.profile_id)
        )
        query_friend = select(self.model).where(self.model.id == cmd.friend_id)
        answer_profile = await self.session.execute(query_profile)
        answer_friend = await self.session.execute(query_friend)
        profile = answer_profile.scalars().first()
        friend = answer_friend.scalars().first()
        profile.friends.append(friend)
        await self.session.commit()
        return {"message": "Friend has been added"}

    async def delete_friends(self, cmd: MatingSchema) -> dict[str:str]:
        query_profile = (
            select(self.model)
            .options(joinedload(self.model.friends))
            .where(self.model.id == cmd.profile_id)
        )
        query_friend = select(self.model).where(self.model.id == cmd.friend_id)
        answer_profile = await self.session.execute(query_profile)
        answer_friend = await self.session.execute(query_friend)
        profile = answer_profile.scalars().first()
        friend = answer_friend.scalars().first()
        profile.friends.remove(friend)
        await self.session.commit()
        return {"message": "Friend has been removed"}

    async def get_profile_with_friends(self, profile_id: UUID) -> FriendsOut | None:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.friends))
            .where(self.model.id == profile_id)
        )
        answer = await self.session.execute(stmt)
        result = answer.unique().scalar_one_or_none()
        return result
