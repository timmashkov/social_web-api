import asyncio
import sys

from fastapi import FastAPI
import uvicorn

from admin_app.admin import admin
from configuration.server import ApiServer
from routes import main_router


def start_app() -> FastAPI:

    app = ApiServer.app_auth

    app.include_router(router=main_router)

    return ApiServer(app, admin).get_app()


if __name__ == "__main__":
    if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    uvicorn.run("main:start_app", reload=True)
