# ---
# lambda-test: false
# ---

from typing import Optional

from fastapi import FastAPI, Header
from pydantic import BaseModel

import modal

web_app = FastAPI()
stub = modal.Stub("example-fastapi-app")
image = modal.Image.debian_slim()


class Item(BaseModel):
    name: str


@web_app.get("/")
async def handle_root(user_agent: Optional[str] = Header(None)):
    print(f"GET /     - received user_agent={user_agent}")
    return "Hello World"


@web_app.post("/foo")
async def handle_foo(item: Item, user_agent: Optional[str] = Header(None)):
    print(f"POST /foo - received user_agent={user_agent}, item.name={item.name}")
    return item


@stub.asgi(image=image)
def fastapi_app():
    return web_app


@stub.webhook(method="POST")
def f(item: Item):
    return "Hello " + item.name


if __name__ == "__main__":
    stub.deploy("webapp")
