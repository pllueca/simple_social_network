from uuid import UUID

from social_network.core.repositories.interfaces.models import User
from social_network.core.repositories.interfaces.user import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users: dict[UUID, User] = {}

    def add(self, user: User) -> None:
        self._users[user.id] = user

    def get(self, user_id: UUID) -> User | None:
        return self._users.get(user_id)

    def list(self) -> list[User]:
        return list(self._users.values())

    def get_by_username(self, username: str) -> User | None:
        for user in self._users.values():
            if user.username == username:
                return user
        return None


USER_REPO = InMemoryUserRepository()
