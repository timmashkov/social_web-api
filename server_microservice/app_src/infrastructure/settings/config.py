import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class ServerConfig(BaseSettings):
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: int = os.environ.get("DB_PORT")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    db_url: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    echo: bool = False

    SECRET: str = os.environ.get("SECRET_KEY")

    REDIS_HOST: str = os.environ.get("REDIS_HOST")
    REDIS_PORT: str = os.environ.get("REDIS_PORT")
    EXPIRATION: int = 60
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"

    RABBIT_NAME: str = os.environ.get("RABBIT_NAME")
    RABBIT_PASS: str = os.environ.get("RABBIT_PASS")
    RABBIT_HOST: str = os.environ.get("RABBIT_HOST")
    RABBIT_PORT: int = os.environ.get("RABBIT_PORT")
    RMQ_URL: str = f"amqp://{RABBIT_NAME}:{RABBIT_PASS}@{RABBIT_HOST}:{RABBIT_PORT}/"


settings = ServerConfig()
