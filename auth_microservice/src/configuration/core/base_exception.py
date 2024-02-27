from fastapi import HTTPException, status

from utils.handys.str_helper import NotEmptyStr


class BaseAPIException(HTTPException):
    """Базовый эксепшн"""

    message: NotEmptyStr | str | None = "Base API Exception"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: NotEmptyStr | None = None) -> None:
        if message is not None:
            self.message = message

        super().__init__(status_code=self.status_code, detail=self.message)
