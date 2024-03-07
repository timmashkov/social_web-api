from contextlib import asynccontextmanager
from fastapi import FastAPI

from configuration.broker import mq, rpc
from utils.handys.rabbit_helper import send_profiles_rpc, send_groups_rpc


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mq.mq_connect()
    rpc.channel = mq.channel
    await rpc.consume_queue(send_profiles_rpc, "rpc_queue")
    await rpc.consume_queue(send_groups_rpc, "rpc_queue")
    yield
    await mq.mq_close_conn()
