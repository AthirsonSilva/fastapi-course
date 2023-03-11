from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = Body(..., gt=0, lt=10)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/v1/posts")
async def say_hello(request: Post):
    bah = request.dict()
    return {"message": bah}
