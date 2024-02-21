from core.base_exception import BaseAPIException
from fastapi import status


class UserNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "User not found"


class UserAlreadyExist(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "User already exist"


class WrongPassword(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Wrong password"
