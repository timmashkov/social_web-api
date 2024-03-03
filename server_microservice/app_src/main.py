from contextlib import asynccontextmanager

import aio_pika
from fastapi import FastAPI
import uvicorn
from aio_pika import IncomingMessage

from core.config.server import mq, rpc
from core.config.server_config import RMQ_URL


@asynccontextmanager
async def lifespan(app: FastAPI):
    await listen()
    await rpc.consume_queue(get_rpc, "task_queue")
    yield
    await mq.mq_close_conn()


async def listen():
    connection = await aio_pika.connect_robust(RMQ_URL)
    channel = await connection.channel()
    rpc.channel = channel
    queue = await channel.declare_queue("task_queue", durable=True)
    await queue.consume(get_msg, no_ack=True)


server_api = FastAPI(
    title="Server microservice of social-web",
    lifespan=lifespan
)


async def get_msg(msg: IncomingMessage):
    txt = msg.body.decode("utf-8")
    print(f"Got {txt}")
    return msg


async def get_rpc(**kwargs):
    print(kwargs)
    return {"status": "ok"}



@server_api.get("/")
async def hello():
    return {"message": "Hello World!"}


if __name__ == "__main__":
    uvicorn.run("main:server_api", reload=True)
