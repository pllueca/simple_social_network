from uuid import uuid4, UUID
from datetime import datetime
from social_network.core.repositories.interfaces.models import User, Post
from social_network.core.repositories.interfaces.user import UserRepository
from social_network.core.repositories.interfaces.post import PostRepository
from social_network.core.services.common import ResourceMissingError


def create_user(username: str, user_repo: UserRepository) -> User:
    # check if exists a user with this username.
    if user_repo.get_by_username(username) is not None:
        raise ValueError(f"Already exists User with name {username}")
    user = User(id=uuid4(), username=username, created_at=datetime.now())
    user_repo.add(user)
    return user


def get_user(user_id: UUID, user_repo: UserRepository) -> User | None:
    return user_repo.get(user_id)


def get_users(user_repo: UserRepository) -> list[User]:
    return user_repo.list()


def get_username_id(username: str, user_repo: UserRepository) -> UUID:
    if (user := user_repo.get_by_username(username)) is None:
        raise ResourceMissingError(f"No User with username {username}")
    return user.id


def create_post(
    user_id: UUID,
    title: str,
    body: str,
    post_repo: PostRepository,
) -> Post:
    post = Post(
        id=uuid4(),
        author_id=user_id,
        title=title,
        body=body,
        created_at=datetime.now(),
    )
    post_repo.add(post)
    return post


def get_post(post_id: UUID, post_repo: PostRepository):
    return post_repo.get(post_id)


def list_all_posts(post_repo: PostRepository):
    return post_repo.list()


def list_posts_by_author(author_id: UUID, post_repo: PostRepository) -> list[Post]:
    return post_repo.list_by_author(author_id)
