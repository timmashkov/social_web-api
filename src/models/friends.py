from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .profile import Profile


class Friend(Base):
    __tablename__ = "friend"
    __table_args__ = [
        UniqueConstraint("user_id", "friend_id", name="idx_unique_profile_friend")
    ]

    profile_id: Mapped[UUID] = mapped_column(ForeignKey("profile.id"))
    friend_id: Mapped[UUID] = mapped_column(ForeignKey("profile.id"))

    profile_link: Mapped["Profile"] = relationship(back_populates="friends")
