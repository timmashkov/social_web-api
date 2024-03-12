import asyncio

import pytest

from configuration.core.database import test_connector
from models import Base


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with test_connector.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_connector.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
