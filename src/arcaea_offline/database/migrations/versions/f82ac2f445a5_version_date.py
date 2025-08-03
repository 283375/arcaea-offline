"""version date

Revision ID: f82ac2f445a5
Revises: 0ca6733e40dc
Create Date: 2025-07-19 17:11:27.448574

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "f82ac2f445a5"
down_revision: Union[str, None] = "0ca6733e40dc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "version_date",
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("songlist_at", sa.DateTime(), nullable=False),
        sa.Column("published_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("version", name=op.f("pk_version_date")),
    )


def downgrade() -> None:
    op.drop_table("version_date")
