import aio_pika
from aio_pika import IncomingMessage

from infrastructure.settings.config import settings


async def listen():
    connection = await aio_pika.connect_robust(settings.RMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("task_queue", durable=True)
    await queue.consume(get_msg, no_ack=True)


async def get_msg(msg: IncomingMessage):
    tokens = msg.body.decode("utf-8")
    print(f"Got {tokens}")
    return tokens
