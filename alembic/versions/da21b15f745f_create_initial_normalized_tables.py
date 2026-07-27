"""create_initial_normalized_tables

Revision ID: da21b15f745f
Revises:
Create Date: 2026-07-27 08:59:41.045855

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "da21b15f745f"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
