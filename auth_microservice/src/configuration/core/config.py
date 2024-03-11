import os
from typing import Literal

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class DevConfig(BaseSettings):
    """Конфиг со всеми чувствительными данными"""

    # apllication mode
    mode: Literal["DEV", "TEST", "PROD"]
    # main database
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: int = os.environ.get("DB_PORT")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    db_url: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    echo: bool = False
    # test database
    TEST_DB_HOST: str = os.environ.get("TEST_DB_HOST")
    TEST_DB_PORT: int = os.environ.get("TEST_DB_PORT")
    TEST_DB_NAME: str = os.environ.get("TEST_DB_NAME")
    TEST_DB_USER: str = os.environ.get("TEST_DB_USER")
    TEST_DB_PASS: str = os.environ.get("TEST_DB_PASS")
    test_db_url: str = (
        f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
    )
    test_echo: bool = False
    # secrets
    SECRET: str = os.environ.get("SECRET_KEY")
    # redis
    REDIS_HOST: str = os.environ.get("REDIS_HOST")
    REDIS_PORT: str = os.environ.get("REDIS_PORT")
    EXPIRATION: int = 60
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    # rabbitmq
    RABBIT_NAME: str = os.environ.get("RABBIT_NAME")
    RABBIT_PASS: str = os.environ.get("RABBIT_PASS")
    RABBIT_HOST: str = os.environ.get("RABBIT_HOST")
    RABBIT_PORT: int = os.environ.get("RABBIT_PORT")
    RMQ_URL: str = f"amqp://{RABBIT_NAME}:{RABBIT_PASS}@{RABBIT_HOST}:{RABBIT_PORT}/"


base_config = DevConfig()
