from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, column_property, relationship
from sqlalchemy import String, Text, func, Date, ForeignKey

from infrastructure.database.models import Base

if TYPE_CHECKING:
    from .guest import Guest


class Ticket(Base):
    __tablename__ = "ticket"

    series: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )
    exp_date: Mapped[Date] = mapped_column(Date, unique=False, nullable=False)
    last_time = column_property(func.datediff(created_at, exp_date))

    guest_id: Mapped[UUID] = mapped_column(
        ForeignKey("guest.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    owner: Mapped["Guest"] = relationship(
        "Guest",
        back_populates="tickets",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
