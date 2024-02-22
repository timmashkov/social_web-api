from fastapi import FastAPI
import uvicorn

from configuration.server import ApiServer
from routes import main_router


def start_app() -> FastAPI:

    app_auth = FastAPI(title="Social web auth microservice")

    app_auth.include_router(router=main_router)

    return ApiServer(app_auth).get_app()


if __name__ == "__main__":
    uvicorn.run("main:start_app", reload=True)
