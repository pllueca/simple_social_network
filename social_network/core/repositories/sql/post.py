from uuid import UUID
from sqlalchemy.orm import Session

from social_network.core.repositories.interfaces.post import PostRepository
from social_network.core.repositories.interfaces.models import Post
from social_network.core.repositories.sql.models.post import Post as PostModel


class SQLPostRepository(PostRepository):
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _post_from_model(post: PostModel) -> Post:
        return Post(
            id=post.id,
            author_id=post.author_id,
            title=post.title,
            body=post.body,
            created_at=post.created_at,
        )

    def add(self, post: Post) -> None:
        new_post = PostModel(
            id=post.id,
            author_id=post.author_id,
            title=post.title,
            body=post.body,
            created_at=post.created_at,
        )
        self.db.add(new_post)
        self.db.commit()
        self.db.refresh(new_post)

    def get(self, post_id: UUID) -> Post | None:
        post = self.db.get(PostModel, post_id)
        if post is None:
            return None
        return self._post_from_model(post)

    def list_by_author(self, author_id: UUID) -> list[Post]:
        posts = self.db.query(PostModel).filter_by(author_id=author_id).all()
        return [self._post_from_model(p) for p in posts]

    def list(self) -> list[Post]:
        posts = self.db.query(PostModel).all()
        return [self._post_from_model(p) for p in posts]
