import abc
from uuid import UUID
from social_network.core.repositories.interfaces.models import Post


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
