from fastapi import FastAPI
import uvicorn
from routes import main_router

app_auth = FastAPI(title="Social web auth microservice")


app_auth.include_router(router=main_router)
# TODO: изменить пароль на SecretStr вместо str
# TODO: продумать логику моделей друзей и тд

if __name__ == "__main__":
    uvicorn.run("main:app_auth", reload=True)
