import heapq
from collections import defaultdict
from datetime import datetime
from uuid import UUID, uuid4

from social_network.core.repositories.interfaces.comment import CommentRepository
from social_network.core.repositories.interfaces.models import Comment, Post, User
from social_network.core.repositories.interfaces.post import PostRepository
from social_network.core.repositories.interfaces.user import UserRepository
from social_network.core.services.common import ResourceMissingError
from social_network.core.services.models import (
    UserAndInteractionsNum,
    UserInteractionsSummary,
)


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


def create_comment(
    author_id: UUID,
    post_id: UUID,
    comment_body: str,
    comment_repo: CommentRepository,
) -> Comment:
    comment = Comment(
        id=uuid4(),
        author_id=author_id,
        post_id=post_id,
        body=comment_body,
        created_at=datetime.now(),
    )
    comment_repo.add(comment)
    return comment


def get_post_comments(post_id: UUID, comment_repo: CommentRepository) -> list[Comment]:
    return comment_repo.get_post_comments(post_id)


def list_comments_by_author(
    author_id: UUID, comments_repo: CommentRepository
) -> list[Comment]:
    return comments_repo.get_user_comments(author_id)


TOP_ELEMENTS = 3


def compute_user_top_interactions(
    user_id: UUID,
    user_repo: UserRepository,
    post_repo: PostRepository,
    comment_repo: CommentRepository,
) -> UserInteractionsSummary:
    user = user_repo.get(user_id)
    if not user:
        raise ResourceMissingError()

    comments_per_author = defaultdict(int)

    # sorted by number of commenters
    posts_and_num_comments = []
    user_posts = list_posts_by_author(user.id, post_repo)
    for post in user_posts:
        comments = get_post_comments(post.id, comment_repo)
        commenters = 0
        for comment in comments:
            if comment.author_id == user_id:
                # dont count own comments
                continue
            commenters += 1
            comments_per_author[comment.author_id] += 1

        # using -commenters to sort ascending
        heapq.heappush(posts_and_num_comments, (-commenters, post.id))

    # key is user id, value is total number of times they comented on the current user
    popular_post_ids = [
        t[1] for t in heapq.nsmallest(TOP_ELEMENTS, posts_and_num_comments)
    ]

    top_users_more_commented = []
    for user_id, num_comments in sorted(
        comments_per_author.items(),
        key=lambda t: t[1],
        reverse=True,
    )[:TOP_ELEMENTS]:
        top_users_more_commented.append(
            UserAndInteractionsNum(
                user_id=user_id,
                num_interactions=num_comments,
            )
        )

    user_comments = list_comments_by_author(user.id, comment_repo)
    users_more_commented_on = defaultdict(int)
    for comment in user_comments:
        # get author of post
        # TODO inneficient! we can query comments w/ original post author
        author_post = get_post(comment.post_id, post_repo).author_id
        users_more_commented_on[author_post] += 1

    top_users_more_commented_on = []
    for user_id, num_comments in sorted(
        users_more_commented_on.items(),
        key=lambda t: t[1],
        reverse=True,
    )[:TOP_ELEMENTS]:
        top_users_more_commented_on.append(
            UserAndInteractionsNum(
                user_id=user_id,
                num_interactions=num_comments,
            )
        )

    return UserInteractionsSummary(
        user_id=user.id,
        most_popular_posts=popular_post_ids,
        users_more_commented_incoming=top_users_more_commented,
        users_more_commented_outcoming=top_users_more_commented_on,
    )
