from datetime import datetime
from uuid import UUID

from sqlalchemy import String, Integer, Text, ForeignKey, func, inspect
from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .users import User
    from .groups import Group


class Profile(Base):
    """Таблица профиля"""

    __tablename__ = "profile"

    first_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    age: Mapped[str] = mapped_column(Integer, unique=False, nullable=False)
    city: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    occupation: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)
    bio: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    user_link: Mapped["User"] = relationship(
        "User",
        back_populates="profile_link",
    )

    friends: Mapped[list["Profile"]] = relationship(
        "Profile",
        secondary="friend",
        primaryjoin="Profile.id==Friend.profile_id",
        secondaryjoin="Profile.id==Friend.friend_id",
    )

    groups: Mapped[list["Group"]] = relationship("Group", back_populates="subscribers")

    posts: Mapped[list["ProfilePost"]] = relationship(
        "ProfilePost", back_populates="author"
    )


class ProfilePost(Base):
    __tablename__ = "Profile_post"

    title: Mapped[str] = mapped_column(String(30), unique=False, nullable=False)
    hashtag: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)
    text: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    written_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )

    post_author: Mapped[UUID] = mapped_column(
        ForeignKey("profile.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    author: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="posts",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
