import sys

sys.path.append("/Users/pllueca/Code/simple_social_network")

from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException
from social_network.core.repositories.interfaces.models import User
from social_network.core.repositories.interfaces.user import (
    UserRepository,
)
from social_network.core.repositories.sql.user import SQLUserRepository
from social_network.core.repositories.sql.db import get_session
from social_network.core.services import service

app = FastAPI()


def get_user_repo() -> UserRepository:
    db = get_session()
    try:
        return SQLUserRepository(db)
    finally:
        db.close()
        print("session closed")


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
