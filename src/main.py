import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from src import models
from src.schemas import PostBase, PostCreate, PostUpdate, PostResponse
from src.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"Hello World"}


@app.post("/api/v1/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create(request: PostCreate, db: Session = Depends(get_db)):
    post = models.Post(**request.dict())

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@app.get("/api/v1/posts/latest", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def find_latest(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()

    if not latest_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found!")

    return latest_post


@app.get("/api/v1/posts", response_model=list[PostResponse], status_code=status.HTTP_200_OK)
async def find_all(db: Session = Depends(get_db)):
    post_list = db.query(models.Post).all()
    return post_list


@app.get("/api/v1/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def find_one(post_id: str, db: Session = Depends(get_db)):
    try:
        if not id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID field is required!")

        found_post = db.query(models.Post).filter(models.Post.id == post_id).first()

        if not found_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post_id} not found!")

        return found_post

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format!")


@app.delete("/api/v1/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(post_id: str, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == post_id).first()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post_id} not found!")

        db.delete(post)
        db.commit()

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format!")

    return "Post deleted successfully!"


@app.put("/api/v1/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def update(post_id: str, request: PostUpdate, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == post_id).first()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Post with id: {post_id} not found!")

        request = request.dict(exclude_unset=True)

        for field, value in request.items():
            setattr(post, field, value)

        post.updated_at = datetime.utcnow()

        db.add(post)
        db.commit()
        db.refresh(post)

        return post

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid data. Please check your request and try again!")
