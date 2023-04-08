import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from src import models
from src.schemas import PostBase, CreatePost, UpdatePost
from src.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"Hello World"}


@app.post("/api/v1/posts")
async def create(request: CreatePost, db: Session = Depends(get_db)):
    post = models.Post(**request.dict())

    db.add(post)
    db.commit()

    db.refresh(post)

    return post


@app.get("/api/v1/posts/latest")
async def find_latest(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()

    if not latest_post:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {id} not found!")

    return latest_post


@app.get("/api/v1/posts")
async def find_all(db: Session = Depends(get_db)) -> dict:
    post_list = db.query(models.Post).all()
    return post_list


@app.get("/api/v1/posts/{post_id}")
async def find_one(post_id: str, db: Session = Depends(get_db)):
    try:
        if not id:
            raise HTTPException(status_code=400, detail="ID field is required!")

        found_post = db.query(models.Post).filter(models.Post.id == post_id).first()

        if not found_post:
            raise HTTPException(
                status_code=404, detail=f"Post with id: {post_id} not found!")

        return found_post

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

    return "Post deleted successfully!"


@app.put("/api/v1/posts/{post_id}")
async def update(post_id: str, request: UpdatePost, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == post_id).first()

        if not post:
            raise HTTPException(
                status_code=404, detail=f"Post with id: {post_id} not found!")

        request = PostBase(**request.dict())
        post.title = request.title or post.title
        post.content = request.content or post.content
        post.published = request.published or post.published
        post.updated_at = datetime.utcnow()

        db.add(post)
        db.commit()
        db.refresh(post)

        return post

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format!")
