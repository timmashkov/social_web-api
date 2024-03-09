from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, column_property, relationship
from sqlalchemy import String, Text, func, Date

from infrastructure.database.models import Base

if TYPE_CHECKING:
    from .guest import Guest


class Event(Base):
    __tablename__ = "event"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    event_date: Mapped[Date] = mapped_column(Date, unique=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )
    last_time = column_property(
        func.concat(
            func.extract("epoch", event_date) - func.extract("epoch", created_at)
        )
    )

    guests: Mapped[list["Guest"]] = relationship("Guest", back_populates="event_link")
