from src.domain import User
from src.implementations.in_memory import USER_REPO
from src.service import create_user, get_users


def main():
    print("Hello from simple-social-network!")

    create_user("maki", USER_REPO)
    create_user("puru", USER_REPO)
    create_user("fg", USER_REPO)
    create_user("mar", USER_REPO)
    create_user("pau", USER_REPO)

    users = get_users(USER_REPO)

    print(users)


if __name__ == "__main__":
    main()
