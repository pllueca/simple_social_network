from social_network.core.repositories.interfaces.models import User
from social_network.core.repositories.interfaces.user import UserRepository

from social_network.core.services.service import create_user, get_users

from social_network.core.repositories.sql.user import SQLUserRepository
from social_network.core.repositories.sql.db import get_session
from social_network.core.services import service


def get_user_repo() -> UserRepository:
    db = get_session()
    return SQLUserRepository(db)


def main():
    print("Hello from simple-social-network!")
    user_repo = get_user_repo()

    # create_user("maki", user_repo())
    # create_user("puru", user_repo())
    # create_user("fg", user_repo())
    # create_user("mar", user_repo())
    # create_user("pau", user_repo)

    users = get_users(user_repo)

    print(users)


if __name__ == "__main__":
    main()
