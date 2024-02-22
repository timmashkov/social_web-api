from typing import TypeVar

from fastapi import FastAPI


FastAPIInstance = TypeVar("FastAPIInstance", bound="FastAPI")


class ApiServer:
    def __init__(self, app: FastAPI):
        self.__app = app

    def get_app(self) -> FastAPIInstance:
        return self.__app
