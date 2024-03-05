from models import Group
from repositories.groups import GroupRepository
from fastapi import Depends

from schemas.group import (
    GroupSearchById,
    GroupSearchByTitle,
    GroupOut,
    GroupIn,
    GroupUpdateIn,
)
from services.cache_service import CacheService
from utils.exceptions.group_exceptions import GroupNotFound, GroupAlreadyExist


class GroupService:
    def __init__(
        self,
        group_repo: GroupRepository = Depends(GroupRepository),
        cache_repo: CacheService = Depends(CacheService),
    ):
        self.group_repo = group_repo
        self.cache_repo = cache_repo

    async def get_all_groups(self) -> list[Group]:
        answer = await self.group_repo.get_all()
        await self.cache_repo.read_cache("created_group")
        return answer

    async def search_group_by_id(self, cmd: GroupSearchById) -> GroupOut:
        answer = await self.group_repo.get_group_by_id(cmd=cmd)
        if not answer:
            raise GroupNotFound
        await self.cache_repo.read_cache("created_group")
        return answer

    async def search_group_by_title(self, cmd: GroupSearchByTitle) -> GroupOut:
        answer = await self.group_repo.get_group_by_title(cmd=cmd)
        if not answer:
            raise GroupNotFound
        await self.cache_repo.read_cache("created_group")
        return answer

    async def register_group(self, cmd: GroupIn) -> GroupOut:
        if not self.search_group_by_title(cmd=GroupSearchByTitle(title=cmd.title)):
            answer = await self.group_repo.create_group(cmd=cmd)
            await self.cache_repo.create_cache("created_group", value=answer)
            return answer
        raise GroupAlreadyExist

    async def edit_group(
        self, cmd: GroupUpdateIn, group_id: GroupSearchById
    ) -> GroupOut:
        if not self.search_group_by_title(cmd=GroupSearchByTitle(title=cmd.title)):
            raise GroupNotFound
        answer = await self.group_repo.update_group(cmd=cmd, group_id=group_id)
        await self.cache_repo.create_cache("created_group", value=answer)
        return answer

    async def drop_group(self, cmd: GroupSearchById) -> GroupOut:
        if not self.search_group_by_title(cmd=GroupSearchByTitle(title=cmd.title)):
            raise GroupNotFound
        answer = await self.group_repo.delete_group(cmd=cmd)
        await self.cache_repo.delete_cache("created_group")
        return answer
