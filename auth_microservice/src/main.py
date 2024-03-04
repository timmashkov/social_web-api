import asyncio
import sys

from fastapi import FastAPI
import uvicorn

from admin_app import admin
from configuration.broker import mq
from configuration.server import ApiServer
from routes import main_router


def start_app() -> FastAPI:

    app = ApiServer.app_auth

    app.include_router(router=main_router)

    @app.get("/mq_send_message")
    async def mq_send_message(text: str):
        """
        EndPoint для отправки сообщения в сервис B.

        В данном примере используется для удобного тригера отправки сообщения в другой сервис.
        """
        routing_key = "social_web"  # Название очереди которую слушает сервис B

        # Публикация сообщения.
        await mq.send_message(routing_key, text)
        return {"succsess"}

    return ApiServer(app, admin).get_app()


if __name__ == "__main__":
    if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    uvicorn.run("main:start_app", reload=True)
