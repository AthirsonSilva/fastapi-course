import uuid
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.Post import Post
from src.posts import posts
from src import models
from src.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/sql")
def test(db: Session = Depends(get_db)):
    return db.query(models.Post).all()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/v1/posts")
async def create(request: Post):
    post_dict = request.dict()
    post_dict["id"] = uuid.uuid4()
    posts.append(post_dict)

    return {"message": "Post created successfully!", "data": post_dict}


@app.get("/api/v1/posts/latest")
async def find_latest() -> dict:
    post = posts[-1]

    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} not found!")

    return {"data": post}


@app.get("/api/v1/posts")
async def find_all(db: Session = Depends(get_db)) -> dict:
    post_list = db.query(models.Post).all()
    return {"data": post_list}


@app.get("/api/v1/posts/{id}")
async def find_one(post_id: str):
    try:
        post = [post for post in posts if post["id"] == post_id]

        if not post:
            raise HTTPException(
                status_code=404, detail=f"Post with id: {post_id} not found!")

        return {"data": post[0]}

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format!")


@app.delete("/api/v1/posts/{id}")
async def delete(post_id: str):
    try:
        post = [post for post in posts if post["id"] == post_id]

        if not post:
            raise HTTPException(
                status_code=404, detail=f"Post with id: {post_id} not found!")

        posts.remove(post[0])

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format!")

    return {"message": "Post deleted successfully!"}


@app.put("/api/v1/posts/{id}")
async def update(post_id: str, request: Post):
    try:
        for index, post in enumerate(posts):
            if post["id"] == post_id:
                posts[index] = request.dict()
                posts[index]["id"] = post_id

                return {"message": "Post updated successfully!", "data": posts[index]}

        raise HTTPException(
            status_code=404, detail=f"Post with id: {post_id} not found!")

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format!")
