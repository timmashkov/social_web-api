from infrastructure.exceptions.base import BaseAPIException
from fastapi import status


class ArticleNotFound(BaseAPIException):
    message = "Article Not Found"
    status_code = status.HTTP_404_NOT_FOUND
