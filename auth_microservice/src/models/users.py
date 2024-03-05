from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Boolean, func

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .profile import Profile


class User(Base):
    """Таблица юзера"""

    __tablename__ = "user"

    login: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    token: Mapped[str] = mapped_column(
        Text, unique=True, nullable=True, server_default="", default=""
    )
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )

    profile_link: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user_link",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
