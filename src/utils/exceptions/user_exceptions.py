from core.base_exception import BaseAPIException


class UserNotFound(BaseAPIException):
    status_code = 404
    message = "User not found"


class UserAlreadyExist(BaseAPIException):
    status_code = 422
    message = "User already exist"


class WrongPassword(BaseAPIException):
    status_code = 401
    message = "Wrong password"
