from infrastructure.exceptions.base import BaseAPIException
from fastapi import status


class TicketNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Ticket not found"


class TicketAlreadyExist(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Ticket already exist"
