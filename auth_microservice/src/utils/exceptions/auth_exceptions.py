from configuration.core.base_exception import BaseAPIException
from fastapi import status


class InvalidScopeToken(BaseAPIException):
    message = "Invalid scope for token."
    status_code = status.HTTP_401_UNAUTHORIZED


class RefreshTokenExpired(BaseAPIException):
    message = "Refresh token expired."
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidRefreshToken(BaseAPIException):
    message = "Invalid refresh token."
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenExpired(BaseAPIException):
    message = "Token expired."
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidToken(BaseAPIException):
    message = "Invalid token."
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenDeleted(BaseAPIException):
    message = "Token deleted"
    status_code = status.HTTP_204_NO_CONTENT


class InvalidCredentials(BaseAPIException):
    message = "Could not validate credentials."
    status_code = status.HTTP_403_FORBIDDEN


class Unauthorized(BaseAPIException):
    message = "User is not authorized"
    status_code = status.HTTP_401_UNAUTHORIZED


class NoRights(BaseAPIException):
    message = "User have not enough rights"
    status_code = status.HTTP_403_FORBIDDEN


class Unapproved(BaseAPIException):
    message = "User is not approved"
    status_code = status.HTTP_401_UNAUTHORIZED
