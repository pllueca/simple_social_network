from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BaseDataModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)


class User(BaseDataModel):
    username: str


class Post(BaseDataModel):
    author_id: UUID  # user id
    title: str
    body: str


class Comment(BaseDataModel):
    author_id: UUID  # user id
    post_id: UUID
    body: str


class Follower(BaseDataModel):
    followed_id: UUID  # user id
    follower_id: UUID  # user id
