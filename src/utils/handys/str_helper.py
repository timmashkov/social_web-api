from pydantic.v1.utils import update_not_none
from pydantic.v1.validators import constr_length_validator


class NotEmptyStr(str):
    """Checks string length"""

    min_length: int | None = 1
    max_length: int | None = None

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, str]) -> None:
        update_not_none(
            field_schema,
            type='string',
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
