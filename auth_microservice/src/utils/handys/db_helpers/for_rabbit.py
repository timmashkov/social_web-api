from configuration.core.database import connector

from sqlalchemy import select

from models import Profile, Group


async def get_profiles():
    async with connector.engine.connect() as session:
        stmt = select(Profile).order_by(Profile.id)
        answer = await session.execute(stmt)
        result = answer.mappings().all()
        data = [dict(row) for row in result]
        return data


async def get_groups():
    async with connector.engine.connect() as session:
        stmt = select(Group).order_by(Group.id)
        answer = await session.execute(stmt)
        result = answer.mappings().all()
        data = [dict(row) for row in result]
        return data
