from contextlib import asynccontextmanager

import aio_pika
from fastapi import FastAPI
import uvicorn
from aio_pika import IncomingMessage

from infrastructure.settings.config import settings
from presentation import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await listen()
    yield


async def listen():
    connection = await aio_pika.connect_robust(settings.RMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("task_queue", durable=True)
    await queue.consume(get_msg, no_ack=True)


server_api = FastAPI(title="Server microservice of social-web")
server_api.include_router(router=main_router)


async def get_msg(msg: IncomingMessage):
    txt = msg.body.decode("utf-8")
    print(f"Got {txt}")
    return msg


async def get_rpc(**kwargs):
    print(kwargs)
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:server_api", reload=True)
