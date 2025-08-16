import sys

sys.path.append("/Users/pllueca/Code/simple_social_network")

from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from social_network.core.repositories.interfaces.comment import CommentRepository
from social_network.core.repositories.interfaces.models import Comment, Post, User
from social_network.core.repositories.interfaces.post import PostRepository
from social_network.core.repositories.interfaces.user import UserRepository
from social_network.core.repositories.sql.comment import SQLCommentRepository
from social_network.core.repositories.sql.db import get_session
from social_network.core.repositories.sql.post import SQLPostRepository
from social_network.core.repositories.sql.user import SQLUserRepository
from social_network.core.services import comments as comments_service
from social_network.core.services import service

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",  # vite frontend dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@dataclass
class Repos:
    user: UserRepository
    post: PostRepository
    comment: CommentRepository


# repository instantiation
def get_user_repo() -> UserRepository:
    db = get_session()
    try:
        return SQLUserRepository(db)
    finally:
        db.close()


def get_post_repo() -> PostRepository:
    db = get_session()
    try:
        return SQLPostRepository(db)
    finally:
        db.close()


def get_all_repos() -> Repos:
    db = get_session()
    try:
        return Repos(
            user=SQLUserRepository(db),
            post=SQLPostRepository(db),
            comment=SQLCommentRepository(db),
        )
    finally:
        db.close()


@app.post("/users", response_model=User)
def create_user(username: str, user_repo: UserRepository = Depends(get_user_repo)):
    user = service.create_user(username, user_repo)
    return user


@app.get("/users", response_model=list[User])
def list_users(user_repo: UserRepository = Depends(get_user_repo)):
    return service.get_users(user_repo)


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: UUID, user_repo: UserRepository = Depends(get_user_repo)):
    user = service.get_user(user_id, user_repo)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/posts", response_model=list[Post])
def list_posts(post_repo: PostRepository = Depends(get_post_repo)):
    return service.list_all_posts(post_repo)


@app.get("/posts/{post_id}", response_model=Post)
def get_post(post_id: UUID, post_repo: PostRepository = Depends(get_post_repo)):
    post = service.get_post(post_id, post_repo)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.get("/posts/{post_id}/comments", response_model=list[Comment])
def get_post_comments(post_id: UUID, repos: Repos = Depends(get_all_repos)):
    if service.get_post(post_id, repos.post) is None:
        raise HTTPException(status_code=404)
    return comments_service.get_post_comments(post_id, repos.comment)


@app.post("/posts", response_model=Post)
def create_post(
    user_id: UUID,
    title: str,
    body: str,
    repos: Repos = Depends(get_all_repos),
):
    user = service.get_user(user_id, repos.user)
    if not user:
        # could be 400 bad request too.
        raise HTTPException(status_code=404, detail="User not found")
    return service.create_post(user_id, title, body, repos.post)


@app.get("/users/{user_id}/posts", response_model=list[Post])
def list_user_posts(
    user_id: UUID,
    repos: Repos = Depends(get_all_repos),
):
    user = service.get_user(user_id, repos.user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return service.list_posts_by_author(user.id, repos.post)


@app.post("/comment", response_model=Comment)
def create_comment(
    post_id,
    author_id,
    body,
    repos: Repos = Depends(get_all_repos),
) -> Comment:

    if service.get_user(author_id, repos.user) is None:
        raise HTTPException(status_code=404)

    if service.get_post(post_id, repos.post) is None:
        raise HTTPException(status_code=404)

    return comments_service.create_comment(
        author_id=author_id,
        post_id=post_id,
        comment_body=body,
        comment_repo=repos.comment,
    )
