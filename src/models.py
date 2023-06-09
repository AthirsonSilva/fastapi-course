import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, UUID, Text, text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(UUID, primary_key=True, index=True, unique=True, default=uuid.uuid4,
                server_default=text("uuid_generate_v4()"))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, default=False, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, server_default=text("now()"))
    owner_id = Column(UUID, ForeignKey("user.id", ondelete='CASCADE'), nullable=False)

    owner = relationship("User", back_populates="posts")


class User(Base):
    __tablename__ = "user"

    id = Column(UUID, primary_key=True, index=True, unique=True, default=uuid.uuid4,
                server_default=text("uuid_generate_v4()"))
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, server_default=text("now()"))

    posts = relationship("Post", back_populates="owner")


class Vote(Base):
    __tablename__ = "vote"

    user_id = Column(UUID, ForeignKey("user.id", ondelete='CASCADE'), primary_key=True)
    post_id = Column(UUID, ForeignKey("post.id", ondelete='CASCADE'), primary_key=True)
