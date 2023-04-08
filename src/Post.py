from typing import Optional
import uuid
from pydantic import BaseModel
from fastapi import Body


class Post(BaseModel):
    id: Optional[uuid.UUID] = None
    title: str
    content: str
    published: bool = False
