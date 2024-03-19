from models import Group
from repositories.groups import GroupRepository
from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from schemas.group import (
    GroupSearchById,
    GroupSearchByTitle,
    GroupOut,
    GroupIn,
    GroupUpdateIn,
    GroupPostIn,
    GroupPostOut,
    GetGroupPostById,
    GroupPostUpd,
)
from services.cache_service import CacheService
from utils.exceptions.group_exceptions import (
    GroupNotFound,
    GroupAlreadyExist,
    GroupPostNotFound,
)


class GroupService:

    def __init__(
        self,
        group_repo: GroupRepository = Depends(GroupRepository),
        cache_repo: CacheService = Depends(CacheService),
    ):
        self.group_repo = group_repo
        self.cache_repo = cache_repo
        self._key = str(self.__class__)

    async def get_all_groups(self) -> list[Group]:
        answer = await self.group_repo.get_all()
        await self.cache_repo.read_cache(self._key)
        return answer

    async def search_group_by_id(self, cmd: GroupSearchById) -> GroupOut:
        answer = await self.group_repo.get_group_by_id(cmd=cmd)
        if not answer:
            raise GroupNotFound
        await self.cache_repo.read_cache(self._key)
        return answer

    async def search_group_by_title(self, cmd: GroupSearchByTitle) -> GroupOut:
        answer = await self.group_repo.get_group_by_title(cmd=cmd)
        if not answer:
            raise GroupNotFound
        await self.cache_repo.read_cache(self._key)
        return answer

    async def register_group(self, cmd: GroupIn) -> GroupOut:
        try:
            answer = await self.group_repo.create_group(cmd=cmd)
            await self.cache_repo.create_cache(self._key, value=answer)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise GroupAlreadyExist

    async def create_group_post(self, cmd: GroupPostIn) -> GroupPostOut:
        try:
            answer = await self.group_repo.create_group_post(cmd=cmd)
            await self.cache_repo.create_cache(self._key, value=answer)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise GroupPostNotFound

    async def edit_group(
        self, cmd: GroupUpdateIn, group_id: GroupSearchById
    ) -> GroupOut:
        if not self.search_group_by_title(cmd=GroupSearchByTitle(title=cmd.title)):
            raise GroupNotFound
        answer = await self.group_repo.update_group(cmd=cmd, group_id=group_id)
        await self.cache_repo.create_cache(self._key, value=answer)
        return answer

    async def edit_group_post(
        self, cmd: GroupPostUpd, group_id: GetGroupPostById
    ) -> GroupPostOut:
        if not self.group_repo.get_group_post_by_id(cmd=group_id):
            raise GroupNotFound
        answer = await self.group_repo.update_group_post(cmd=cmd, post_id=group_id)
        await self.cache_repo.create_cache(self._key, value=answer)
        return answer

    async def drop_group(self, cmd: GroupSearchById) -> GroupOut:
        if not self.search_group_by_id(cmd=GroupSearchById(id=cmd.id)):
            raise GroupNotFound
        answer = await self.group_repo.delete_group(cmd=cmd)
        await self.cache_repo.delete_cache(self._key)
        return answer

    async def drop_group_post(self, cmd: GetGroupPostById) -> GroupPostOut:
        if not self.search_group_by_id(cmd=GroupSearchById(id=cmd.id)):
            raise GroupNotFound
        answer = await self.group_repo.delete_group_post(cmd=cmd)
        await self.cache_repo.delete_cache(self._key)
        return answer
