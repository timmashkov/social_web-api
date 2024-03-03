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
    def deserialize_data(data: bytes) -> Any:
        return json.loads(data)


class MessageQueue(BaseMQ):
    """Класс брокера, имплементирует коннкект и ченл, посылает мессагу и слушает очередь"""

    async def mq_connect(self):
        self.connection = await aio_pika.connect_robust(self.mq_url)
        self.channel = await self.connection.channel()
        print("RabbitMQ connection is now available")

    async def mq_close_conn(self):
        await self.connection.close()

    async def send_message(self, queue_name: str, data: Any):
        """Отправка месседжа в один конец"""
        # это сообщение получит консумер
        message = Message(
            body=self.serialize_data(data=data),
            content_type="application/social_web",
            correlation_id=str(uuid4()),
        )
        # паблишинг в дефолтную очередь
        await self.channel.default_exchange.publish(message, queue_name)

    async def listen_queue(self, func, queue_name: str, auto_delete: bool = False):
        """Прослушивание очереди"""
        # создание очереди
        queue = await self.channel.declare_queue(
            queue_name, auto_delete=auto_delete, durable=True
        )
        # асинк итерирование очереди
        async with queue.iterator() as que_iter:
            async for message in que_iter:
                await func(message)


mq = MessageQueue(settings.RMQ_URL)


class CoreRPC(BaseMQ):
    futures = {}

    @staticmethod
    async def del_consumer(queue, consumers):
        for key, val in consumers.items():
            await queue.cancel(key)

    def on_response(self, message: IncomingMessage):
        future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)
        message.ack()

    async def call(self, queue_name: str, **kwargs):
        """
        RPC-метод для отправки в другой сервис с целью возврата ответа из другого сервиса.

        Данный метод на каждый вызов создает уникальную очередь
        тем самым не скапливая в одной очереди множество запросов.

        Важно!!! Узнать в лучший способ использования создания анонимных очередей.
        """
        # Создание уникальной очереди на которую будет возвращен ответ из другого сервиса.
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

        # Magic #1
        future = self.channel.loop.create_future()

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

        # Magic #2 Выполняется только после того как другой сервис пришлет запрос.
        response = await future

        # Magic #3 Удаление слушателей.
        # Почему-то даже с auto_delete очередь после выполнения не удаляется ссылаясь на консумера.
        # Поэтому решение было вручную удалять консумера после выполнения задачи.
        await self.del_consumer(callback_queue, consumers)

        return self.deserialize_data(response)

    async def consume_queue(self, func, queue_name: str):
        """Прослушивание очереди брокера."""
        queue = await self.channel.declare_queue(queue_name, durable=True)

        # Все очереди обрабатываются одной общей функцией.
        # В нее передается exchange, func и сам message.

        # Exchange используется для возврата ответа используя метод publish.

        # partial работает как генерировании функции с аргументами,
        # Если пройтись по стеку тогда там на выходе будет что-то подобного on_call_message(message, exchange, func)
        print(1)
        await queue.consume(
            partial(self.on_call_message, self.channel.default_exchange, func)
        )

    async def on_call_message(self, exchange, func, message: IncomingMessage):
        """Единая функция для приема message из других сервисов и отправки обратно ответа."""
        payload = self.deserialize_data(message.body)
        try:
            print(payload, "test")
            result = await func(**payload)
            print(result)
        except Exception as e:
            result = self.serialize_data(dict(error="error", reason=str(e)))

        result = self.serialize_data(result)

        await exchange.publish(
            Message(body=result, correlation_id=message.correlation_id),
            routing_key=message.reply_to,
        )
        await message.ack()


rpc = CoreRPC(settings.RMQ_URL)
