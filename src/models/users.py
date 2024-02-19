from sqlalchemy import String, Integer, Text

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    age: Mapped[str] = mapped_column(Integer, unique=False, nullable=False)
    city: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    occupation: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)
    bio: Mapped[str] = mapped_column(Text, unique=False, nullable=True)


