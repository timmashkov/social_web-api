from configuration.core.base_exception import BaseAPIException
from fastapi import status


class ProfileNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Profile not found"


class ProfileAlreadyExist(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Profile already exist"


class FriendNotExist(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Friend not found"


class ProfilePostNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Post not found"


class ProfilePostAlreadyExist(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Post already exist"
