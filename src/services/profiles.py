from uuid import UUID

from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from models import Profile
from repositories.profile import ProfileRepository
from schemas.profile import ProfileOut, ProfileIn
from utils.exceptions.profile_exceptions import ProfileNotFound, ProfileAlreadyExist


class ProfileService:
    def __init__(self, prof_repo: ProfileRepository = Depends(ProfileRepository)):
        self.prof_repo = prof_repo

    async def get_profiles(self) -> list[Profile]:
        answer = await self.prof_repo.get_all()
        return answer

    async def get_profile(self, profile_id: UUID) -> ProfileOut:
        answer = await self.prof_repo.get_profile_by_id(profile_id=profile_id)
        if not answer:
            raise ProfileNotFound
        return answer

    async def add_profile(self, data: ProfileIn) -> ProfileOut:
        try:
            answer = await self.prof_repo.create_profile(data=data)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise ProfileAlreadyExist

    async def change_profile(self, data: ProfileIn, profile_id: UUID) -> ProfileOut:
        if await self.prof_repo.get_profile_by_id(profile_id=profile_id):
            return await self.prof_repo.update_profile(data=data, profile_id=profile_id)
        raise ProfileNotFound

    async def drop_profile(self, profile_id: UUID) -> dict[str:str]:
        if await self.prof_repo.get_profile_by_id(profile_id=profile_id):
            return await self.prof_repo.delete_profile(profile_id=profile_id)
        raise ProfileNotFound
