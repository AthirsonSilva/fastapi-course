import uuid

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


def password_verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def convert_uuid_to_string(posts):
    return [{**post, "id": str(post["id"])} if isinstance(post["id"], uuid.UUID) else post for post in posts]
