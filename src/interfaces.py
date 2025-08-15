import abc
from src.domain import User, Post
from uuid import UUID


class UserRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, user_id: UUID) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> list[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError


class PostRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, post: Post) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, post_id: UUID) -> Post | None:
        raise NotImplementedError

    @abc.abstractmethod
    def list_by_author(self, author_id: UUID) -> list[Post]:
        raise NotImplementedError
