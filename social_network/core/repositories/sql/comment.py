from uuid import UUID

from sqlalchemy.orm import Session

from social_network.core.repositories.interfaces.comment import CommentRepository
from social_network.core.repositories.interfaces.models import Comment
from social_network.core.repositories.sql.models.comment import Comment as CommentModel


class SQLCommentRepository(CommentRepository):

    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _comment_from_model(comment: CommentModel) -> Comment:
        return Comment(
            id=comment.id,
            author_id=comment.author_id,
            post_id=comment.post_id,
            body=comment.body,
            created_at=comment.created_at,
        )

    def add(self, comment: Comment) -> None:
        new_comment = CommentModel(
            id=comment.id,
            author_id=comment.author_id,
            post_id=comment.post_id,
            body=comment.body,
            created_at=comment.created_at,
        )
        self.db.add(new_comment)
        self.db.commit()
        self.db.refresh(new_comment)

    def get(self, comment_id: UUID) -> Comment | None:
        comment = self.db.get(CommentModel, comment_id)
        if not comment:
            return None
        return self._comment_from_model(comment)

    def get_post_comments(self, post_id) -> list[Comment]:
        comments = self.db.query(CommentModel).filter_by(post_id=post_id).all()
        return [self._comment_from_model(comment) for comment in comments]

    def get_user_comments(self, author_id) -> list[Comment]:
        comments = self.db.query(CommentModel).filter_by(author_id=author_id).all()
        return [self._comment_from_model(comment) for comment in comments]
