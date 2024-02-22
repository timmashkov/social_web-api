from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from configuration.core.config import base_config


class SessionConnector:
    def __init__(self, url: str, echo: bool) -> None:
        self._engine = create_async_engine(url=url, echo=echo)
        self._session_fabric = async_sessionmaker(
            bind=self._engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def scoped_session(self) -> AsyncGenerator:
        async with self._session_fabric() as session:
            yield session
            await session.close()


connector = SessionConnector(base_config.db_url, base_config.echo)
