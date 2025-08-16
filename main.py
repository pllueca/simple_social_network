from uuid import UUID
from social_network.core.repositories.interfaces.models import User, Post
from social_network.core.repositories.interfaces.user import UserRepository
from social_network.core.repositories.interfaces.post import PostRepository
from social_network.core.repositories.interfaces.comment import CommentRepository

from social_network.core.services.service import (
    create_user,
    get_users,
    get_post,
    create_post,
    list_all_posts,
    list_posts_by_author,
)
import random
from social_network.core.services.comments import create_comment, get_post_comments

from social_network.core.repositories.sql.user import SQLUserRepository
from social_network.core.repositories.sql.post import SQLPostRepository
from social_network.core.repositories.sql.comment import SQLCommentRepository
from social_network.core.repositories.sql.db import get_session


def get_repos() -> tuple[UserRepository, PostRepository, CommentRepository]:
    db = get_session()
    return SQLUserRepository(db), SQLPostRepository(db), SQLCommentRepository(db)


def post_text():
    r = random.randint(1, 4)
    match r:
        case 1:
            return """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed placerat facilisis nisl quis mattis. Donec fermentum nisi quis porta dignissim. Duis vestibulum placerat massa ac porttitor. Aliquam mattis enim metus, ac volutpat nulla commodo eu. Aliquam luctus risus metus, sit amet rutrum nibh euismod nec. Vestibulum eget finibus nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; In iaculis a sem vel blandit. Maecenas nec lacus a lacus cursus lobortis. Proin pellentesque dolor quis dui hendrerit mattis. Curabitur risus elit, hendrerit non orci et, suscipit volutpat odio. Vestibulum imperdiet sem eu nisi commodo, fermentum mollis lectus elementum. Sed rhoncus quis ante eget elementum. Integer fermentum nisl eu orci scelerisque mattis ut id turpis. Phasellus luctus vel libero eget dapibus."""
        case 2:
            return "helo helo helo"
        case 3:
            return "meow " * random.randint(1, 7)
        case 4:
            return """list of things:
* 1
* other thing
* something else """

        case _:
            return "empty post"


def post_title(idx):
    r = random.randint(1, 4)
    match r:
        case 1:
            return "boring post"
        case 2:
            return "helo helo helo"
        case 3:
            return "meow "
        case _:
            return f"my {idx}th post"


def create_data():

    user_repo, post_repo, comment_repo = get_repos()

    usernames = [
        "maki",
        "puru",
        "fg",
        "mar",
        "pau",
    ]
    usernames_to_ids: dict[str, UUID] = {}
    for u in usernames:
        user = create_user(u, user_repo)
        usernames_to_ids[u] = user.id

        # each user have between 0, 5 posts
        for i in range(random.randint(0, 5)):
            create_post(
                user.id,
                title=post_title(i),
                body=post_text(),
                post_repo=post_repo,
            )

    posts = list_all_posts(post_repo)
    for post in posts:
        for i in range(0, 4):
            create_comment(
                random.choice(list(usernames_to_ids.values())),
                post.id,
                "comment",
                comment_repo,
            )


def main():
    print("Hello from simple-social-network!")
    create_data()

    user_repo, post_repo, comment_repo = get_repos()

    users = get_users(user_repo)
    print(users)

    posts = list_all_posts(post_repo)
    print(posts)

    maki_user = user_repo.get_by_username("maki")
    if maki_user is None:
        return
    posts = list_posts_by_author(maki_user.id, post_repo)
    print(posts)

    comments = get_post_comments(posts[0].id, comment_repo)
    print(comments)


if __name__ == "__main__":
    main()
