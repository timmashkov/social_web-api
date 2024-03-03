from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from infrastructure.broker.rabbit_handler import mq
from infrastructure.utils import listen
from presentation import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await listen()
    yield
    await mq.mq_close_conn()


server_api = FastAPI(title="Server microservice of social-web", lifespan=lifespan)
server_api.include_router(router=main_router)


if __name__ == "__main__":
    uvicorn.run("main:server_api", reload=True)
