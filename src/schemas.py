import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, conint


class PostBase(BaseModel):
    id: Optional[uuid.UUID]
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=1000)
    published: bool = Field(...)


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]


class UserBase(BaseModel):
    id: Optional[uuid.UUID]
    email: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    email: Optional[str]
    password: Optional[str]


class UserLogin(BaseModel):
    email: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100)


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserPostModel(PostBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserResponseWithPosts(UserResponse):
    posts: list[UserPostModel]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: Optional[str] = None


class PostResponse(PostBase):
    created_at: datetime
    updated_at: datetime
    owner_id: uuid.UUID
    owner: UserResponse
    count: int

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: uuid.UUID
    direction: conint(ge=-1, le=1)

    class Config:
        orm_mode = True
