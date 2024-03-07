from contextlib import asynccontextmanager
from fastapi import FastAPI

from configuration.broker import mq, rpc
from configuration.core.database import connector

from sqlalchemy import select

from models import Profile


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mq.mq_connect()
    rpc.channel = mq.channel
    await rpc.consume_queue(send_profiles_rpc, "rpc_queue")
    yield
    await mq.mq_close_conn()


async def get_profiles():
    async with connector.engine.connect() as session:
        stmt = select(Profile).order_by(Profile.id)
        answer = await session.execute(stmt)
        result = answer.mappings().all()
        data = [dict(row) for row in result]
        return data


async def send_profiles_rpc():
    return await get_profiles()
