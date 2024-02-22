from core.base_exception import BaseAPIException
from fastapi import status


class ProfileNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Profile not found"


class ProfileAlreadyExist(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Profile already exist"
