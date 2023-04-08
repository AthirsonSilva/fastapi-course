import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from src import models
from src.Post import Post
from src.database import engine, get_db
from src.posts import posts

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/v1/posts")
async def create(request: Post, db: Session = Depends(get_db)):
    post = models.Post(**request.dict())

    db.add(post)
    db.commit()

    db.refresh(post)

    return {"message": "Post created successfully!", "data": post}


@app.get("/api/v1/posts/latest")
async def find_latest(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()

    if not latest_post:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} not found!")

    return {"data": latest_post}


@app.get("/api/v1/posts")
async def find_all(db: Session = Depends(get_db)) -> dict:
    post_list = db.query(models.Post).all()
    return {"data": post_list}


@app.get("/api/v1/posts/{post_id}")
async def find_one(post_id: str, db: Session = Depends(get_db)):
    try:
        if not id:
            raise HTTPException(status_code=400, detail="ID field is required!")

        found_post = db.query(models.Post).filter(models.Post.id == post_id).first()

        if not found_post:
            raise HTTPException(
                status_code=404, detail=f"Post with id: {post_id} not found!")

        return {"data": found_post}

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format!")


@app.delete("/api/v1/posts/{post_id}")
async def delete(post_id: str, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == post_id).first()

        if not post:
            raise HTTPException(
                status_code=404, detail=f"Post with id: {post_id} not found!")

        db.delete(post)
        db.commit()

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format!")

    return {"message": "Post deleted successfully!"}


@app.put("/api/v1/posts/{post_id}")
async def update(post_id: str, request: Post, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == post_id).first()

        if not post:
            raise HTTPException(
                status_code=404, detail=f"Post with id: {post_id} not found!")

        request = Post(**request.dict())
        post.title = request.title or post.title
        post.content = request.content or post.content
        post.published = request.published or post.published
        post.updated_at = datetime.utcnow()

        db.add(post)
        db.commit()
        db.refresh(post)

        return {"message": "Post updated successfully!", "data": post}

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format!")
