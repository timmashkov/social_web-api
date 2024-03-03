import os

from dotenv import load_dotenv

load_dotenv()

RABBIT_NAME = os.environ.get("RABBIT_NAME")
RABBIT_PASS = os.environ.get("RABBIT_PASS")
RABBIT_HOST = os.environ.get("RABBIT_HOST")
RABBIT_PORT = os.environ.get("RABBIT_PORT")
RMQ_URL: str = f"amqp://{RABBIT_NAME}:{RABBIT_PASS}@{RABBIT_HOST}:{RABBIT_PORT}/"