from contextlib import asynccontextmanager
from fastapi import FastAPI

from configuration.broker import mq


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mq.mq_connect()
    yield
    await mq.mq_close_conn()
