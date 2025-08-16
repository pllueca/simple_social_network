from sqlalchemy import Column, Integer, String, DateTime, UUID, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from social_network.core.repositories.sql.db import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID, primary_key=True)
    author_id = Column(UUID, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title = Column(String(120), nullable=False)
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
