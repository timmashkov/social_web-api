from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from infrastructure.broker.rabbit_handler import mq, rpc
from presentation import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mq.mq_connect()
    rpc.channel = mq.channel
    yield
    await mq.mq_close_conn()


server_api = FastAPI(title="Server microservice of social-web", lifespan=lifespan)
server_api.include_router(router=main_router)


if __name__ == "__main__":
    uvicorn.run("main:server_api", reload=True, port=1111)
