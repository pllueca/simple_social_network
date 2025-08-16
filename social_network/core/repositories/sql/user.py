from uuid import UUID
from sqlalchemy.orm import Session

from social_network.core.repositories.interfaces.user import UserRepository, User
from social_network.core.repositories.sql.models.user import User as UserModel


class SQLUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, user: User) -> None:
        new_user = UserModel(
            id=user.id,
            username=user.username,
            created_at=user.created_at,
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

    def get(self, user_id: UUID) -> User | None:
        user = self.db.get(UserModel, user_id)
        if user is None:
            return None
        return User(
            id=user.id,
            username=user.username,
            created_at=user.created_at,
        )

    def list(self) -> list[User]:
        users = self.db.query(UserModel).all()
        return [
            User(
                id=user.id,
                username=user.username,
                created_at=user.created_at,
            )
            for user in users
        ]

    def get_by_username(self, username: str) -> User | None:
        user = self.db.query(UserModel).filter_by(username=username).first()
        if user is None:
            return None
        return User(
            id=user.id,
            username=user.username,
            created_at=user.created_at,
        )
