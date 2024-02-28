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


class GroupService:
    def __init__(self, group_repo: GroupRepository = Depends(GroupRepository)):
        self.group_repo = group_repo

    async def get_all_groups(self) -> list[Group]:
        answer = await self.group_repo.get_all()
        return answer

    async def search_group_by_id(self, cmd: GroupSearchById) -> GroupOut:
        answer = await self.group_repo.get_group_by_id(cmd=cmd)
        return answer

    async def search_group_by_title(self, cmd: GroupSearchByTitle) -> GroupOut:
        answer = await self.group_repo.get_group_by_title(cmd=cmd)
        return answer

    async def register_group(self, cmd: GroupIn) -> GroupOut:
        answer = await self.group_repo.create_group(cmd=cmd)
        return answer

    async def edit_group(
        self, cmd: GroupUpdateIn, group_id: GroupSearchById
    ) -> GroupOut:
        answer = await self.group_repo.update_group(cmd=cmd, group_id=group_id)
        return answer

    async def drop_group(self, cmd: GroupSearchById) -> GroupOut:
        answer = await self.group_repo.delete_group(cmd=cmd)
        return answer
