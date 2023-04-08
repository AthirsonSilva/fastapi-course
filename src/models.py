import uuid

from sqlalchemy import Column, Integer, String, Boolean, UUID

from .database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(UUID, primary_key=True, index=True, unique=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, default=False)
