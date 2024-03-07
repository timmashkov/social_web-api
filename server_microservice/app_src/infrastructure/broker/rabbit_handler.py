import asyncio
import copy
import json
from functools import partial
from typing import Any
from uuid import uuid4

import aio_pika
from aio_pika.message import Message, IncomingMessage

from infrastructure.settings.config import settings


class BaseMQ:
    """Базовый класс для брокера, принимает ЮРЛ, содержит статики для энкода/декода"""

    def __init__(self, mq_url: str) -> None:
        self.mq_url = mq_url
        self.connection = None
        self.channel = None

    @staticmethod
    def serialize_data(data: Any) -> bytes:
        return json.dumps(data).encode()

    @staticmethod
    def deserialize_data(data: bytes | list[str]) -> Any:
        return json.loads(data)


class MessageQueue(BaseMQ):
    """Класс брокера, имплементирует коннкект и ченл, посылает мессагу и слушает очередь"""

    async def mq_connect(self):
        self.connection = await aio_pika.connect_robust(self.mq_url)
        self.channel = await self.connection.channel()
        print(f"RabbitMQ connection {self.mq_url} is now available")

    async def mq_close_conn(self):
        print(f"RabbitMQ connection {self.mq_url} has benn closed")
        await self.connection.close()

    async def send_message(self, queue_name: str, data: Any):
        message = Message(
            body=self.serialize_data(data=data),
            content_type="application/social_web",
            correlation_id=str(uuid4()),
        )
        await self.channel.default_exchange.publish(message, queue_name)

    async def listen_queue(self, func, queue_name: str, auto_delete: bool = False):
        queue = await self.channel.declare_queue(
            queue_name, auto_delete=auto_delete, durable=True
        )
        async with queue.iterator() as que_iter:
            async for message in que_iter:
                await func(message)

    async def get_message(self, queue_name: str, no_ack: bool = True):
        messages = []

        async def func(msg: IncomingMessage):
            data = self.deserialize_data(msg.body)
            messages.append(data)
            print(data)
            return data

        queue = await self.channel.declare_queue(
            queue_name, auto_delete=False, durable=True
        )
        await queue.consume(func, no_ack)

        return messages


mq = MessageQueue(settings.RMQ_URL)


class RPC(BaseMQ):
    futures = {}

    @staticmethod
    async def cancel_consumer(queue, consumers):
        """
        Удаление из очереди слушателей
        """
        for key, val in consumers.items():
            await queue.cancel(key)

    async def on_response(self, message: IncomingMessage):
        """
        Функция которая обрабатывает приходящий ответ из другого сервиса

        """
        future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)
        await message.ack()

    async def call(self, queue_name: str, **kwargs):
        """
        RPC-метод для отправки в другой сервис с целью возврата ответа из другого сервиса.

        """
        callback_queue = await self.channel.declare_queue(
            exclusive=True, auto_delete=True, durable=True
        )
        await callback_queue.consume(
            self.on_response
        )  # Метод класса который обрабатывает ответ
        consumers = copy.copy(
            callback_queue._consumers
        )  # Копирование консумеров для удаления очереди из раббита

        correlation_id = str(uuid4())

        loop = asyncio.get_event_loop()
        future = loop.create_future()
        self.futures[correlation_id] = future

        await self.channel.default_exchange.publish(
            Message(
                body=self.serialize_data(kwargs),
                content_type="application/json",
                correlation_id=correlation_id,
                reply_to=callback_queue.name,
            ),
            routing_key=queue_name,
            mandatory=True,
        )

        # Выполняется только после того как другой сервис пришлет запрос.
        response = await future

        # Удаление слушателей.
        await self.cancel_consumer(callback_queue, consumers)

        return self.deserialize_data(response)

    async def consume_queue(self, func, queue_name: str):
        """Прослушивание очереди брокера."""
        queue = await self.channel.declare_queue(queue_name)
        await queue.consume(
            partial(self.on_call_message, self.channel.default_exchange, func)
        )

    async def on_call_message(self, exchange, func, message: IncomingMessage):
        """Единая функция для приема message из других сервисов и отправки обратно ответа."""
        payload = self.deserialize_data(message.body)
        try:
            result = await func(**payload)
        except Exception as e:
            result = self.serialize_data(dict(error="error", reason=str(e)))

        result = self.serialize_data(result)

        await exchange.publish(
            Message(body=result, correlation_id=message.correlation_id),
            routing_key=message.reply_to,
        )
        await message.ack()


rpc = RPC(settings.RMQ_URL)
