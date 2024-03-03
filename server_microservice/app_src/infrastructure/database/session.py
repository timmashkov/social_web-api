from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from infrastructure.settings.config import settings


class SessionAdaptor:
    def __init__(self, url: str, echo: bool) -> None:
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def session_local(self) -> AsyncGenerator:
        async with self.session_factory() as session:
            yield session
            await session.close()


connector = SessionAdaptor(url=settings.db_url, echo=settings.echo)
