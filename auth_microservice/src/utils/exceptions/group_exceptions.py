from configuration.core.base_exception import BaseAPIException
from fastapi import status


class GroupNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Group not found"


class GroupAlreadyExist(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Group already exist"
