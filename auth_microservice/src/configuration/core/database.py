from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import NullPool

from configuration.core.config import base_config


class SessionConnector:
    """Коннектор к сессии алхимии"""

    def __init__(self, url: str, echo: bool) -> None:
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_fabric = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def scoped_session(self) -> AsyncGenerator:
        async with self.session_fabric() as session:
            yield session
            await session.close()


connector = SessionConnector(base_config.db_url, base_config.echo)


class TestSessionConnector:
    """Тестовый коннектор к сессии алхимии"""

    def __init__(self, url: str, echo: bool) -> None:
        self.engine = create_async_engine(url=url, echo=echo, poolclass=NullPool)
        self.session_fabric = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def scoped_session(self) -> AsyncGenerator:
        async with self.session_fabric() as session:
            yield session
            await session.close()


test_connector = TestSessionConnector(base_config.test_db_url, base_config.test_echo)
