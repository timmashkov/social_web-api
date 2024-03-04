import aio_pika
from aio_pika import IncomingMessage

from infrastructure.broker.rabbit_handler import mq
from infrastructure.settings.config import settings


async def listen():
    await mq.mq_connect()
    await mq.get_message(get_msg, "social_web")


async def get_msg(msg: IncomingMessage):
    tokens = msg.body.decode("utf-8")
    print(f"Got {msg}: {tokens}")


async def iter_messages():
    await mq.mq_connect()
    await mq.listen_queue(get_msg, "social_web")
