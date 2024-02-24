from typing import TypeVar

from fastapi import FastAPI
from sqladmin import Admin

FastAPIInstance = TypeVar("FastAPIInstance", bound="FastAPI")


class ApiServer:
    app_auth = FastAPI(title="Social web auth microservice")

    def __init__(self, app: FastAPI, admin_panel: Admin):
        self.__app = app
        self.__admin_panel = admin_panel

    def get_app(self) -> FastAPIInstance:
        return self.__app

    def get_admin(self):
        return self.__admin_panel
