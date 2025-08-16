"""create posts table

Revision ID: eca2e3facc78
Revises: 1f3be8ffc109
Create Date: 2025-08-16 07:58:26.123536

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "eca2e3facc78"
down_revision: Union[str, Sequence[str], None] = "1f3be8ffc109"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("author_id", sa.UUID, sa.ForeignKey("users.id")),
        sa.Column("title", sa.String(120), nullable=False),
        sa.Column("body", sa.Text()),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
