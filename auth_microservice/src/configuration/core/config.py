import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class DevConfig(BaseSettings):
    """Конфиг со всеми чувствительными данными"""

    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: int = os.environ.get("DB_PORT")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    db_url: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    echo: bool = True

    SECRET: str = os.environ.get("SECRET_KEY")

    REDIS_HOST: str = os.environ.get("REDIS_HOST")
    REDIS_PORT: str = os.environ.get("REDIS_PORT")


base_config = DevConfig()
