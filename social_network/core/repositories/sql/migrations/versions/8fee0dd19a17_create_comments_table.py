"""create comments table

Revision ID: 8fee0dd19a17
Revises: eca2e3facc78
Create Date: 2025-08-16 12:09:53.906192

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8fee0dd19a17"
down_revision: Union[str, Sequence[str], None] = "eca2e3facc78"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "comments",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("author_id", sa.UUID, sa.ForeignKey("users.id")),
        sa.Column("post_id", sa.UUID, sa.ForeignKey("posts.id")),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("comments")
