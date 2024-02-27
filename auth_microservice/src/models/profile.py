from uuid import UUID

from sqlalchemy import String, Integer, Text, ForeignKey
from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .users import User
    from .friends import Friend


class Profile(Base):
    __tablename__ = "profile"

    first_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    age: Mapped[str] = mapped_column(Integer, unique=False, nullable=False)
    city: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    occupation: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)
    bio: Mapped[str] = mapped_column(Text, unique=False, nullable=True)

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
