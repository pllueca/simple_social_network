from datetime import datetime, timezone

from sqlalchemy import UUID, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from social_network.core.repositories.sql.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
