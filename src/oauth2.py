from datetime import datetime, timedelta

import jwt

from src.config import settings


def create_access_token(sub: dict):
    to_encode = sub.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {"access_token": encoded_jwt, "token_type": "bearer"}
