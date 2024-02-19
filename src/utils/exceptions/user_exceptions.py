from core.base_exception import BaseAPIException


class UserNotFound(BaseAPIException):
    status_code = 404
    message = "User not found"
