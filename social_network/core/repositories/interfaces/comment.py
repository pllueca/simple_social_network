import abc

from social_network.core.repositories.interfaces.models import Comment


class CommentRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, comment: Comment):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, comment_id) -> Comment | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_post_comments(self, post_id) -> list[Comment]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_comments(self, author_id) -> list[Comment]:
        raise NotImplementedError
