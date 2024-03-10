from contextlib import asynccontextmanager
from fastapi import FastAPI

from configuration.broker import mq, rpc
from utils.handys.rabbit_helper import send_data_rpc


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mq.mq_connect()
    rpc.channel = mq.channel
    await rpc.consume_queue(send_data_rpc, "rpc_queue")
    yield
    await mq.mq_close_conn()
