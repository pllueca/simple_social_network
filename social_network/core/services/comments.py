from datetime import datetime
from uuid import UUID, uuid4

from social_network.core.repositories.interfaces.comment import CommentRepository
from social_network.core.repositories.interfaces.models import Comment, Post, User
from social_network.core.repositories.interfaces.post import PostRepository
from social_network.core.repositories.interfaces.user import UserRepository
from social_network.core.services.common import ResourceMissingError


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
