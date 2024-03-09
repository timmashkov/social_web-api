from infrastructure.exceptions.base import BaseAPIException
from fastapi import status


class EventNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Event not found"


class EventAlreadyExist(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Event already exist"
