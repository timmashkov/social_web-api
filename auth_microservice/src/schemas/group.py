from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GroupSearchById(BaseModel):
    id: UUID


class GroupSearchByTitle(BaseModel):
    title: str


class GroupUpdateIn(GroupSearchByTitle):
    description: str


class GroupIn(GroupUpdateIn):
    group_admin: UUID


class GroupOut(GroupIn, GroupSearchById):
    is_official: bool
    created_at: datetime | str
