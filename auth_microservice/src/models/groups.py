from datetime import datetime
from uuid import UUID

from sqlalchemy import String, Text, Boolean, ForeignKey, func
from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .profile import Profile


class Group(Base):
    __tablename__ = "group"

    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    is_official: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )

    group_admin: Mapped[UUID] = mapped_column(
        ForeignKey("profile.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    subscribers: Mapped[list["Profile"]] = relationship(
        "Profile",
        back_populates="groups",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )

    group_posts: Mapped[list["GroupPost"]] = relationship(
        "GroupPost", back_populates="community"
    )


class GroupPost(Base):
    __tablename__ = "group_post"

    header: Mapped[str] = mapped_column(String(30), unique=False, nullable=False)
    hashtag: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)
    body: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    written_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )

    group_author: Mapped[UUID] = mapped_column(
        ForeignKey("group.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    community: Mapped["Group"] = relationship(
        "Group",
        back_populates="group_posts",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
