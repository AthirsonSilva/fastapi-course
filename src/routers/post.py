from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src import models
from src.database import get_db
from src.schemas import PostCreate, PostUpdate, PostResponse

import src.oauth2 as oauth2

router = APIRouter(
    prefix="/api/v1/posts",
    tags=["Posts resources"],
)


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create(request: PostCreate, db: Session = Depends(get_db),
                 current_user: models.User = Depends(oauth2.get_current_user)):
    post = models.Post(owner_id=current_user.id, **request.dict())

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.get("/latest", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def find_latest(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()

    if not latest_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found!")

    return latest_post


@router.get("", response_model=list[PostResponse], status_code=status.HTTP_200_OK)
async def find_all(db: Session = Depends(get_db)):
    post_list = db.query(models.Post).all()
    return post_list


@router.get("/my-posts", response_model=list[PostResponse], status_code=status.HTTP_200_OK)
async def find_by_user(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_list = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return post_list


@router.get("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
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


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(post_id: str, db: Session = Depends(get_db),
                 current_user: models.User = Depends(oauth2.get_current_user)):
    try:
        post = db.query(models.Post).filter(models.Post.id == post_id).first()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post_id} not found!")

        if post.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed to delete this post!")

        db.delete(post)
        db.commit()

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format!")

    return "Post deleted successfully!"


@router.put("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def update(post_id: str, request: PostUpdate, db: Session = Depends(get_db),
                 current_user: models.User = Depends(oauth2.get_current_user)):
    try:
        post = db.query(models.Post).filter(models.Post.id == post_id).first()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Post with id: {post_id} not found!")

        if post.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed to delete this post!")

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
