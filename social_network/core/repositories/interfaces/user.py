import abc
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID, uuid4
from social_network.core.repositories.interfaces.models import User


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
