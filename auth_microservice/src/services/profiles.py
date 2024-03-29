from uuid import UUID

from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from configuration.broker import mq
from models import Profile
from repositories.profile import ProfileRepository
from schemas.profile import (
    ProfileOut,
    ProfileIn,
    MatingSchema,
    FriendsOut,
    ProfileUpdateIn,
    GetProfilePostById,
    ProfilePostOut,
    GetProfilePostByTitle,
    ProfilePostIn,
    ProfileWithPosts,
    ProfileWithGroups,
    ProfileWithFriendsGroups,
    ProfileFull,
)
from services.cache_service import CacheService
from utils.exceptions.profile_exceptions import (
    ProfileNotFound,
    ProfileAlreadyExist,
    FriendNotExist,
    ProfilePostNotFound,
    ProfilePostAlreadyExist,
)


class ProfileService:
    """Сервисный репозиторий для профиля"""

    def __init__(
        self,
        prof_repo: ProfileRepository = Depends(ProfileRepository),
        cache_repo: CacheService = Depends(CacheService),
    ):
        self.prof_repo = prof_repo
        self.cache_repo = cache_repo
        self._key = str(self.__class__)

    async def get_profiles(self) -> list[Profile]:
        answer = await self.prof_repo.get_all()
        await self.cache_repo.read_cache(self._key)
        return answer

    async def get_profile_by_id(self, profile_id: UUID) -> ProfileOut:
        answer = await self.prof_repo.get_profile_by_id(profile_id=profile_id)
        if not answer:
            raise ProfileNotFound
        await self.cache_repo.read_cache(self._key)
        return answer

    async def get_profile_post_id(self, post_id: GetProfilePostById) -> ProfilePostOut:
        answer = await self.prof_repo.get_profile_post_by_id(post_id=post_id)
        if not answer:
            raise ProfilePostNotFound
        await self.cache_repo.read_cache(self._key)
        return answer

    async def get_profile_post_title(
        self, post_title: GetProfilePostByTitle
    ) -> ProfilePostOut:
        answer = await self.prof_repo.get_profile_post_by_title(post_title=post_title)
        if not answer:
            raise ProfilePostNotFound
        await self.cache_repo.read_cache(self._key)
        return answer

    async def add_profile(self, data: ProfileIn) -> ProfileOut:
        try:
            answer = await self.prof_repo.create_profile(data=data)
            await self.cache_repo.create_cache(self._key, value=data)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise ProfileAlreadyExist

    async def add_profile_post(self, data: ProfilePostIn) -> ProfilePostOut:
        try:
            answer = await self.prof_repo.create_profile_post(data=data)
            await self.cache_repo.create_cache(self._key, value=data)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise ProfilePostAlreadyExist

    async def change_profile(
        self, data: ProfileUpdateIn, profile_id: UUID
    ) -> ProfileOut:
        if await self.prof_repo.get_profile_by_id(profile_id=profile_id):
            await self.cache_repo.update_cache(self._key, value=data)
            return await self.prof_repo.update_profile(data=data, profile_id=profile_id)
        raise ProfileNotFound

    async def change_profile_post(
        self, data: ProfilePostIn, post_id: GetProfilePostById
    ) -> ProfilePostOut:
        if await self.prof_repo.get_profile_post_by_id(post_id=post_id):
            await self.cache_repo.update_cache(self._key, value=data)
            return await self.prof_repo.update_profile_post(data=data, post_id=post_id)
        raise ProfilePostNotFound

    async def drop_profile(self, profile_id: UUID) -> dict[str:str]:
        if await self.prof_repo.get_profile_by_id(profile_id=profile_id):
            await self.cache_repo.delete_cache(self._key)
            return await self.prof_repo.delete_profile(profile_id=profile_id)
        raise ProfileNotFound

    async def drop_profile_post(self, post_id: GetProfilePostById) -> dict[str:str]:
        if await self.prof_repo.get_profile_post_by_id(post_id=post_id):
            await self.cache_repo.delete_cache(self._key)
            return await self.prof_repo.delete_profile_post(post_id=post_id)
        raise ProfilePostNotFound

    async def get_friends(self, profile_id: UUID) -> FriendsOut:
        return await self.prof_repo.get_profile_with_friends(profile_id=profile_id)

    async def get_posts(self, profile_id: UUID) -> ProfileWithPosts:
        return await self.prof_repo.get_profile_with_posts(profile_id=profile_id)

    async def get_groups(self, profile_id: UUID) -> ProfileWithGroups:
        return await self.prof_repo.get_profile_with_groups(profile_id=profile_id)

    async def get_friends_groups(self, profile_id: UUID) -> ProfileWithFriendsGroups:
        return await self.prof_repo.get_profile_with_friends_groups(
            profile_id=profile_id
        )

    async def get_profile_full(self, profile_id: UUID) -> ProfileFull:
        return await self.prof_repo.get_full_profile(profile_id=profile_id)

    async def follow(self, data: MatingSchema) -> dict[str:str]:
        if not await self.prof_repo.get_profile_by_id(profile_id=data.profile_id):
            raise ProfileNotFound
        if not await self.prof_repo.get_profile_by_id(profile_id=data.friend_id):
            raise FriendNotExist
        return await self.prof_repo.add_friends(cmd=data)

    async def unfollow(self, data: MatingSchema) -> dict[str:str]:
        if not await self.prof_repo.get_profile_by_id(profile_id=data.profile_id):
            raise ProfileNotFound
        if not await self.prof_repo.get_profile_by_id(profile_id=data.friend_id):
            raise FriendNotExist
        return await self.prof_repo.delete_friends(cmd=data)

    async def send_profiles(self):
        """Special method for sending profiles list to another microservice"""
        answer = await self.prof_repo.get_all()
        routing_key = "sw-feed"
        result = [row.as_dict() for row in answer]
        await mq.send_message(routing_key, data=result)
        return answer
