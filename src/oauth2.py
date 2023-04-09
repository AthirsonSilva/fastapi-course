from datetime import datetime, timedelta

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src import models
from src.config import settings
from src.database import get_db
from src.exceptions import credentials_exception
from src.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def create_access_token(sub: dict):
    to_encode = sub.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {"access_token": encoded_jwt, "token_type": "bearer"}


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if payload.get("exp") < datetime.utcnow():
            raise credentials_exception

        if not payload.get("sub"):
            raise credentials_exception

        return TokenData(sub=payload.get("sub"))

    except jwt.PyJWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_data = verify_access_token(token)

    user = db.query(models.User).filter(models.User.email == token_data.sub).first()

    if not user:
        raise credentials_exception

    return user
