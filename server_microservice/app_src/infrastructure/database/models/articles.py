from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, func

from infrastructure.database.models import Base


class Article(Base):
    __tablename__ = "article"

    title: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    body: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )
