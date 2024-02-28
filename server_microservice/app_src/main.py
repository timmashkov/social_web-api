from fastapi import FastAPI
import uvicorn


server_api = FastAPI(
    title="Server microservice of social-web"
)


@server_api.get("/")
async def hello():
    return {"message": "Hello World!"}


if __name__ == "__main__":
    uvicorn.run("main:server_api", reload=True)
