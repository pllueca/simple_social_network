from datetime import datetime
from pydantic import BaseModel
from uuid import UUID, uuid4


class User(BaseModel):
    id: UUID
    username: str
    created_at: datetime


class Post(BaseModel):
    id: UUID
    author_id: UUID  # user id
    title: str
    body: str
    created_at: datetime


class Comment(BaseModel):
    id: UUID
    author_id: UUID  # user id
    post_id: UUID
    created_at: datetime
    body: str


class Follower(BaseModel):
    followed_id: UUID  # user id
    follower_id: UUID  # user id
    created_at: datetime
