"""v1

Revision ID: b7a0accfc17f
Revises:
Create Date: 2025-06-05 22:17:13.327742

"""

from typing import Any, Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b7a0accfc17f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(
    *,
    data_migration: bool = False,
    data_migration_options: Any = None,
) -> None:
    op.create_table(
        "charts",
        sa.Column("song_id", sa.TEXT(), nullable=False),
        sa.Column("rating_class", sa.INTEGER(), nullable=False),
        sa.Column("name_en", sa.TEXT(), nullable=False),
        sa.Column("name_jp", sa.TEXT()),
        sa.Column("artist", sa.TEXT(), nullable=False),
        sa.Column("bpm", sa.TEXT(), nullable=False),
        sa.Column("bpm_base", sa.REAL(), nullable=False),
        sa.Column("package_id", sa.TEXT(), nullable=False),
        sa.Column("time", sa.INTEGER()),
        sa.Column("side", sa.INTEGER(), nullable=False),
        sa.Column("world_unlock", sa.BOOLEAN(), nullable=False),
        sa.Column("remote_download", sa.BOOLEAN()),
        sa.Column("bg", sa.TEXT(), nullable=False),
        sa.Column("date", sa.INTEGER(), nullable=False),
        sa.Column("version", sa.TEXT(), nullable=False),
        sa.Column("difficulty", sa.INTEGER(), nullable=False),
        sa.Column("rating", sa.INTEGER(), nullable=False),
        sa.Column("note", sa.INTEGER(), nullable=False),
        sa.Column("chart_designer", sa.TEXT()),
        sa.Column("jacket_designer", sa.TEXT()),
        sa.Column("jacket_override", sa.BOOLEAN(), nullable=False),
        sa.Column("audio_override", sa.BOOLEAN(), nullable=False),
        sa.PrimaryKeyConstraint("song_id", "rating_class", name="pk_charts"),
    )

    op.create_table(
        "aliases",
        sa.Column("song_id", sa.TEXT(), nullable=False),
        sa.Column("alias", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("song_id", "alias", name="pk_aliases"),
    )

    op.create_table(
        "packages",
        sa.Column("package_id", sa.TEXT(), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("package_id", name="pk_packages"),
    )

    op.create_table(
        "scores",
        sa.Column("id", sa.INTEGER(), autoincrement=True),
        sa.Column("song_id", sa.TEXT(), nullable=False),
        sa.Column("rating_class", sa.INTEGER(), nullable=False),
        sa.Column("score", sa.INTEGER(), nullable=False),
        sa.Column("pure", sa.INTEGER()),
        sa.Column("far", sa.INTEGER()),
        sa.Column("lost", sa.INTEGER()),
        sa.Column("time", sa.INTEGER(), nullable=False),
        sa.Column("max_recall", sa.INTEGER()),
        sa.Column("clear_type", sa.INTEGER()),
        sa.PrimaryKeyConstraint("id", name="pk_scores"),
        sa.ForeignKeyConstraint(
            ["song_id", "rating_class"],
            ["charts.song_id", "charts.rating_class"],
            name="fk_scores_song_id_charts",
            onupdate="CASCADE",
            ondelete="NO ACTION",
        ),
    )

    properties_tbl = op.create_table(
        "properties",
        sa.Column("key", sa.TEXT(), nullable=False),
        sa.Column("value", sa.TEXT(), nullable=False),
        # according to the commit history this was a unique constraint
        # but i remember sqlalchemy complains if you don't add a primary key
        # anyways above tables have modifications like this too
        # and nobody actualty uses v1 schema so who cares
        sa.PrimaryKeyConstraint("key", name="pk_properties"),
    )

    # there should be CREATE VIEWs here but im skipping them
    # because nobody actually checks this file

    op.execute(sa.insert(properties_tbl).values(key="db_version", value="1"))


def downgrade() -> None:
    raise NotImplementedError("This is the first revision bro")
