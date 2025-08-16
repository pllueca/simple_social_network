from typing import TypedDict
from uuid import UUID

from pydantic import BaseModel


class UserAndInteractionsNum(BaseModel):
    user_id: UUID
    num_interactions: int


class UserInteractionsSummary(BaseModel):
    user_id: UUID
    # users that commented more on us
    users_more_commented_incoming: list[UserAndInteractionsNum]
    # users that we commented more on
    users_more_commented_outcoming: list[UserAndInteractionsNum]
    # post ids of posts with more comments
    most_popular_posts: list[UUID]
