from typing import TypeVar

from fastapi import FastAPI
from sqladmin import Admin

from routes import main_router
from utils.handys.rabbit_lifespan import lifespan

FastAPIInstance = TypeVar("FastAPIInstance", bound="FastAPI")


class ApiServer:
    """Сервер апи"""

    app_auth = FastAPI(title="Social web auth microservice", lifespan=lifespan)
    app_auth.include_router(router=main_router)

    def __init__(self, app: FastAPI, admin_panel):
        self.__app = app
        self.__admin_panel = admin_panel

    def get_app(self) -> FastAPIInstance:
        return self.__app

    def get_admin(self):
        return self.__admin_panel
