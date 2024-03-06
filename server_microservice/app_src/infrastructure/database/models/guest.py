from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, func, ForeignKey

from infrastructure.database.models import Base

if TYPE_CHECKING:
    from .events import Event
    from .tickets import Ticket


class Guest(Base):
    __tablename__ = "guest"

    first_name: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), unique=False, nullable=False)

    event_id: Mapped[UUID] = mapped_column(
        ForeignKey("event.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    event_link: Mapped["Event"] = relationship(
        "Event",
        back_populates="guests",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )

    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="owner")
