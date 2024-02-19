from fastapi import FastAPI
import uvicorn

app_auth = FastAPI(
    title="Social web auth microservice"
)


@app_auth.get("/")
def hello():
    return {"message": "hello"}


if __name__ == "__main__":
    uvicorn.run("main:app_auth", reload=True)
