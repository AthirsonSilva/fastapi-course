import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, UUID, Text, text, TIMESTAMP

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
