from social_network.core.repositories.interfaces.models import User, Post
from social_network.core.repositories.interfaces.user import UserRepository
from social_network.core.repositories.interfaces.post import PostRepository

from social_network.core.services.service import (
    create_user,
    get_users,
    create_post,
    list_all_posts,
    list_posts_by_author,
)

from social_network.core.repositories.sql.user import SQLUserRepository
from social_network.core.repositories.sql.post import SQLPostRepository
from social_network.core.repositories.sql.db import get_session
from social_network.core.services import service


def get_repos() -> tuple[UserRepository, PostRepository]:
    db = get_session()
    return SQLUserRepository(db), SQLPostRepository(db)


def main():
    print("Hello from simple-social-network!")
    user_repo, post_repo = get_repos()

    # maki_user = create_user("maki", user_repo)
    # create_user("puru", user_repo)
    # create_user("fg", user_repo)
    # create_user("mar", user_repo)
    # create_user("pau", user_repo)
    # create_post(maki_user.id, "Miau", "meow meow meow", post_repo)

    users = get_users(user_repo)
    print(users)

    posts = list_all_posts(post_repo)
    print(posts)

    maki_user = user_repo.get_by_username("maki")
    if maki_user is None:
        return
    print(list_posts_by_author(maki_user.id, post_repo))


if __name__ == "__main__":
    main()
