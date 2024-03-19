import asyncio
from typing import AsyncGenerator, Callable, Any

from sqlalchemy.ext.asyncio import AsyncSession

import pytest

from configuration.core.database import test_connector, connector
from configuration.server import ApiServer
from models import Base

from httpx import AsyncClient


app = ApiServer.app_auth

Base.metadata.bind = test_connector.engine


async def override_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    session = test_connector.session_fabric()
    async with session as sess:
        yield sess


app.dependency_overrides[connector.scoped_session] = override_session_dependency


@pytest.fixture(autouse=True, scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    try:
        loop = asyncio.get_event_loop_policy().get_event_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def prepare_database(event_loop):
    async with test_connector.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_connector.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="module")
def saved_data() -> dict[str, Any]:
    return {}


def get_routes() -> dict[str, str]:
    routes = {}
    for route in app.routes:
        routes[route.name] = route.path
    return routes


def reverse(foo: Callable, routes: dict[str, str] = get_routes(), **kwargs) -> str:
    path = routes[foo.__name__]
    return path.format(**kwargs)
