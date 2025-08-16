from sqlalchemy import Column, Integer, String, DateTime, UUID, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from social_network.core.repositories.sql.db import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID, primary_key=True)

    author_id = Column(UUID, ForeignKey("users.id"))
    author = relationship("User", back_populates="comments")

    post_id = Column(UUID, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="comments")

    body = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
