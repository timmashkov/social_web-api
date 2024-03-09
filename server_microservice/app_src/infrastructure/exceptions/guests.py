from infrastructure.exceptions.base import BaseAPIException
from fastapi import status


class GuestNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Guest not found"


class GuestAlreadyExist(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Guest already exist"
