import re
from uuid import UUID

from pydantic.v1.utils import update_not_none
from pydantic.v1.validators import constr_length_validator


class NotEmptyStr(str):
    """Проверяет длину строки"""

    min_length: int | None = 1
    max_length: int | None = None

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, str]) -> None:
        update_not_none(
            field_schema,
            type="string",
            writeOnly=False,
            minLength=cls.min_length,
            maxLength=cls.max_length,
        )

    @classmethod
    def __get_validators__(cls):
        yield constr_length_validator

    def __init__(self, value: str) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"NotEmptyStr('{self}')"


def clean_and_validate_uuid(s):
    s = re.sub(r"[^a-fA-F0-9-]", "", s)
    return s
