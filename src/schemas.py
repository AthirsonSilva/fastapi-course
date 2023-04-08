import uuid
from typing import Optional

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    id: Optional[uuid.UUID]
    title: str
    content: str
    published: bool


class CreatePost(PostBase):
    title: str = Field(...)
    content: str = Field(...)
    published: bool = Field(default=True)


class UpdatePost(PostBase):
    title: Optional[str] = Field(...)
    content: Optional[str] = Field(...)
    published: Optional[bool] = Field(...)
