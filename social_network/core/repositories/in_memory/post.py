from uuid import UUID
from social_network.core.repositories.interfaces.models import Post
from social_network.core.repositories.interfaces.post import PostRepository


class InMemoryPostRepository(PostRepository):
    def __init__(self):
        self._posts: dict[UUID, Post] = {}

    def add(self, post: Post) -> None:
        self._posts[post.id] = post

    def get(self, post_id: UUID) -> Post | None:
        return self._posts.get(post_id)

    def list_by_author(self, author_id: UUID) -> list[Post]:
        return [post for post in self._posts.values() if post.author_id == author_id]

    def list(self) -> list[Post]:
        return [post for post in self._posts.values()]
