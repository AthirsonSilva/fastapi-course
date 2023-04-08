from fastapi import FastAPI

from src.routers import user, post
from src import models
from src.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"Hello World"}

