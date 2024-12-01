from fastapi import FastAPI

from src.handlers.exceptions import APIException
from starlette.exceptions import HTTPException

from src.api.v1.cargo.router import router as cargo_router

app = FastAPI()

app.include_router(cargo_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.add_exception_handler(HTTPException, APIException.handle_exception)
app.add_exception_handler(Exception, APIException.handle_exception)