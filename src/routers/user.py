from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src import models
from src.database import get_db
from src.schemas import UserCreate, UserResponse, UserResponseWithPosts
from src.utils import hash_password

router = APIRouter(
    prefix="/api/v1/users",
    tags=["User resources"],
)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreate, db: Session = Depends(get_db)):
    user = models.User(**request.dict())
    user.password = hash_password(user.password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("", response_model=list[UserResponseWithPosts], status_code=status.HTTP_200_OK)
async def find_all_users(db: Session = Depends(get_db)):
    user_list = db.query(models.User).all()

    return user_list


@router.get("/{user_id}", response_model=UserResponseWithPosts, status_code=status.HTTP_200_OK)
async def find_one_user(user_id: str, db: Session = Depends(get_db)):
    try:
        if not id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID field is required!")

        found_user = db.query(models.User).filter(models.User.id == user_id).first()

        if not found_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {user_id} not found!")

        return found_user

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format!")
