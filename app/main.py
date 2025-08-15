from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException
from src.domain import User, Post
from src.interfaces import UserRepository, PostRepository
from src.implementations.in_memory import USER_REPO
from src import service

app = FastAPI()


def get_user_repo() -> UserRepository:
    return USER_REPO


@app.post("/users", response_model=User)
def create_user(username: str, user_repo: UserRepository = Depends(get_user_repo)):
    user = service.create_user(username, user_repo)
    return user


@app.get("/users", response_model=list[User])
def list_users(user_repo: UserRepository = Depends(get_user_repo)):
    return user_repo.list()


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: UUID, user_repo: UserRepository = Depends(get_user_repo)):
    user = user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
