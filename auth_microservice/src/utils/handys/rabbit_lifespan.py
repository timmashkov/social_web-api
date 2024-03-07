from contextlib import asynccontextmanager
from fastapi import FastAPI

from configuration.broker import mq, rpc


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mq.mq_connect()
    rpc.channel = mq.channel
    yield
    await mq.mq_close_conn()
