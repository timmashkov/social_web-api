from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator


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


class GetGroupPostById(BaseModel):
    id: UUID | str


class GetGroupPostByHeader(BaseModel):
    header: str


class GroupPostUpd(GetGroupPostByHeader):
    hashtag: str
    body: str

    @field_validator("hashtag")
    def check_hashtag(cls, data):
        if data.startswith("#"):
            return data
        raise ValueError("Hashtag must starts with '#'")


class GroupPostIn(GroupPostUpd):
    group_author: UUID


class GroupPostOut(GetGroupPostById, GroupPostIn):
    written_at: datetime | str


class GroupPostOutWithCommunity(GroupPostOut):
    community: GroupOut
