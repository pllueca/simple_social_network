"""create users table

Revision ID: 1f3be8ffc109
Revises:
Create Date: 2025-08-15 22:58:55.075139

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1f3be8ffc109"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
