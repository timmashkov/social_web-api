from typing import TypeVar

from fastapi import FastAPI
from flask import Flask
from fastapi.middleware.wsgi import WSGIMiddleware

FastAPIInstance = TypeVar("FastAPIInstance", bound="FastAPI")


class ApiServer:
    def __init__(self, app: FastAPI, flask_app: Flask):
        self.__app = app
        self._create_flask = flask_app

    def get_app(self) -> FastAPIInstance:
        return self.__app

    @staticmethod
    def _register_flask_app(app: FastAPIInstance, flask_app: Flask):
        app.mount('/admin_panel', WSGIMiddleware(flask_app))
