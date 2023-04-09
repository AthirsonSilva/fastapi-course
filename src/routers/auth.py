from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src import database, schemas, models
from src.oauth2 import create_access_token
from src.utils import password_verify

router = APIRouter(tags=['Authentication resources'], prefix='/api/v1/auth')


@router.post("/login", response_model=dict, status_code=status.HTTP_201_CREATED)
def login(credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid email.")

    if not password_verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Wrong password.")

    return {"access_token": create_access_token(sub={"sub": user.email})}
