import sys

sys.path.append("/Users/pllueca/Code/simple_social_network")

from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException
from social_network.core.repositories.interfaces.models import User, Post
from social_network.core.repositories.interfaces.user import UserRepository
from social_network.core.repositories.interfaces.post import PostRepository
from social_network.core.repositories.sql.user import SQLUserRepository
from social_network.core.repositories.sql.post import SQLPostRepository
from social_network.core.repositories.sql.db import get_session
from social_network.core.services import service

app = FastAPI()


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


def get_user_post_repos() -> tuple[UserRepository, PostRepository]:
    db = get_session()
    try:
        return SQLUserRepository(db), SQLPostRepository(db)
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


@app.post("/posts", response_model=Post)
def create_post(
    user_id: UUID,
    title: str,
    body: str,
    repos: tuple[UserRepository, PostRepository] = Depends(get_user_post_repos),
):
    user_repo, post_repo = repos
    user = service.get_user(user_id, user_repo)
    if not user:
        # could be 400 bad request too.
        raise HTTPException(status_code=404, detail="User not found")
    return service.create_post(user_id, title, body, post_repo)


@app.get("/users/{user_id}/posts", response_model=list[Post])
def list_user_posts(
    user_id: UUID,
    repos: tuple[UserRepository, PostRepository] = Depends(get_user_post_repos),
):
    user_repo, post_repo = repos
    user = service.get_user(user_id, user_repo)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return service.list_posts_by_author(user.id, post_repo)
