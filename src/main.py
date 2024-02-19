from fastapi import FastAPI
import uvicorn

app_auth = FastAPI(title="Social web auth microservice")


if __name__ == "__main__":
    uvicorn.run("main:app_auth", reload=True)
