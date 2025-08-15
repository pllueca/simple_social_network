from uuid import uuid4
from datetime import datetime
from src.domain import User
from src.interfaces import UserRepository


def create_user(username: str, user_repo: UserRepository) -> User:
    # check if exists a user with this username.
    if user_repo.get_by_username(username) is not None:
        raise ValueError("already exists user with this name")
    user = User(id=uuid4(), username=username, created_at=datetime.now())
    user_repo.add(user)
    return user


def get_users(user_repo: UserRepository) -> list[User]:
    return user_repo.list()
