"""v1 to v4

Revision ID: a3f9d48b7de3
Revises: b7a0accfc17f
Create Date: 2024-11-24 00:03:07.697165

"""

from datetime import datetime, timezone
from typing import Mapping, Optional, Sequence, TypedDict, Union

import sqlalchemy as sa
from alembic import context, op

revision: str = "a3f9d48b7de3"
down_revision: Union[str, None] = "b7a0accfc17f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class V4DataMigrationOptions(TypedDict):
    threshold_date: Optional[datetime]


def _data_migration_options(user_input: Optional[Mapping]):
    options: V4DataMigrationOptions = {
        "threshold_date": datetime(year=2017, month=1, day=23, tzinfo=timezone.utc),
    }

    if user_input is None:
        return options

    if not isinstance(user_input, dict):
        raise TypeError("v4 migration: data migration options should be a dict object")

    threshold_date = user_input.get("threshold_date")
    if threshold_date is not None and not isinstance(threshold_date, datetime):
        raise ValueError(
            "v4 migration: threshold_date should be None or a datetime.datetime object"
        )
    options["threshold_date"] = threshold_date

    return options


def upgrade(
    *,
    data_migration: bool = True,
    data_migration_options: Optional[V4DataMigrationOptions] = None,
) -> None:
    data_migration_options = _data_migration_options(data_migration_options)
    threshold_date = data_migration_options["threshold_date"]

    op.create_table(
        "difficulties",
        sa.Column("song_id", sa.TEXT(), nullable=False),
        sa.Column("rating_class", sa.Integer(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("rating_plus", sa.Boolean(), nullable=False),
        sa.Column("chart_designer", sa.TEXT(), nullable=True),
        sa.Column("jacket_desginer", sa.TEXT(), nullable=True),
        sa.Column("audio_override", sa.Boolean(), nullable=False),
        sa.Column("jacket_override", sa.Boolean(), nullable=False),
        sa.Column("jacket_night", sa.TEXT(), nullable=True),
        sa.Column("title", sa.TEXT(), nullable=True),
        sa.Column("artist", sa.TEXT(), nullable=True),
        sa.Column("bg", sa.TEXT(), nullable=True),
        sa.Column("bg_inverse", sa.TEXT(), nullable=True),
        sa.Column("bpm", sa.TEXT(), nullable=True),
        sa.Column("bpm_base", sa.Float(), nullable=True),
        sa.Column("version", sa.TEXT(), nullable=True),
        sa.Column("date", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("song_id", "rating_class", name="pk_difficulties"),
    )
    op.create_table(
        "packs",
        sa.Column("id", sa.TEXT(), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="fk_packs"),
    )
    op.create_table(
        "songs",
        sa.Column("idx", sa.Integer(), nullable=False),
        sa.Column("id", sa.TEXT(), nullable=False),
        sa.Column("title", sa.TEXT(), nullable=False),
        sa.Column("artist", sa.TEXT(), nullable=False),
        sa.Column("set", sa.TEXT(), nullable=False),
        sa.Column("bpm", sa.TEXT(), nullable=True),
        sa.Column("bpm_base", sa.Float(), nullable=True),
        sa.Column("audio_preview", sa.Integer(), nullable=True),
        sa.Column("audio_preview_end", sa.Integer(), nullable=True),
        sa.Column("side", sa.Integer(), nullable=True),
        sa.Column("version", sa.TEXT(), nullable=True),
        sa.Column("date", sa.Integer(), nullable=True),
        sa.Column("bg", sa.TEXT(), nullable=True),
        sa.Column("bg_inverse", sa.TEXT(), nullable=True),
        sa.Column("bg_day", sa.TEXT(), nullable=True),
        sa.Column("bg_night", sa.TEXT(), nullable=True),
        sa.Column("source", sa.TEXT(), nullable=True),
        sa.Column("source_copyright", sa.TEXT(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="songs"),
    )
    op.create_table(
        "charts_info",
        sa.Column("song_id", sa.TEXT(), nullable=False),
        sa.Column("rating_class", sa.Integer(), nullable=False),
        sa.Column(
            "constant",
            sa.Integer(),
            nullable=False,
            comment="real_constant * 10. For example, Crimson Throne [FTR] is 10.4, then store 104.",
        ),
        sa.Column("notes", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["rating_class"],
            ["difficulties.rating_class"],
            name="fk_charts_info_rating_class_difficulties",
        ),
        sa.ForeignKeyConstraint(
            ["song_id"],
            ["difficulties.song_id"],
            name="fk_charts_info_song_id_difficulties",
        ),
        sa.PrimaryKeyConstraint("song_id", "rating_class", name="pk_charts_info"),
    )
    op.create_table(
        "difficulties_localized",
        sa.Column("song_id", sa.TEXT(), nullable=False),
        sa.Column("rating_class", sa.Integer(), nullable=False),
        sa.Column("title_ja", sa.TEXT(), nullable=True),
        sa.Column("title_ko", sa.TEXT(), nullable=True),
        sa.Column("title_zh_hans", sa.TEXT(), nullable=True),
        sa.Column("title_zh_hant", sa.TEXT(), nullable=True),
        sa.Column("artist_ja", sa.TEXT(), nullable=True),
        sa.Column("artist_ko", sa.TEXT(), nullable=True),
        sa.Column("artist_zh_hans", sa.TEXT(), nullable=True),
        sa.Column("artist_zh_hant", sa.TEXT(), nullable=True),
        sa.ForeignKeyConstraint(
            ["rating_class"],
            ["difficulties.rating_class"],
            name="fk_difficulties_localized_rating_class_difficulties",
        ),
        sa.ForeignKeyConstraint(
            ["song_id"],
            ["difficulties.song_id"],
            name="fk_difficulties_localized_song_id_difficulties",
        ),
        sa.PrimaryKeyConstraint(
            "song_id", "rating_class", name="pk_difficulties_localized"
        ),
    )
    op.create_table(
        "packs_localized",
        sa.Column("id", sa.TEXT(), nullable=False),
        sa.Column("name_ja", sa.TEXT(), nullable=True),
        sa.Column("name_ko", sa.TEXT(), nullable=True),
        sa.Column("name_zh_hans", sa.TEXT(), nullable=True),
        sa.Column("name_zh_hant", sa.TEXT(), nullable=True),
        sa.Column("description_ja", sa.TEXT(), nullable=True),
        sa.Column("description_ko", sa.TEXT(), nullable=True),
        sa.Column("description_zh_hans", sa.TEXT(), nullable=True),
        sa.Column("description_zh_hant", sa.TEXT(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id"],
            ["packs.id"],
            name="fk_packs_localized_id_packs",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_packs_localized"),
    )
    op.create_table(
        "songs_localized",
        sa.Column("id", sa.TEXT(), nullable=False),
        sa.Column("title_ja", sa.TEXT(), nullable=True),
        sa.Column("title_ko", sa.TEXT(), nullable=True),
        sa.Column("title_zh_hans", sa.TEXT(), nullable=True),
        sa.Column("title_zh_hant", sa.TEXT(), nullable=True),
        sa.Column("search_title_ja", sa.TEXT(), nullable=True, comment="JSON array"),
        sa.Column("search_title_ko", sa.TEXT(), nullable=True, comment="JSON array"),
        sa.Column(
            "search_title_zh_hans", sa.TEXT(), nullable=True, comment="JSON array"
        ),
        sa.Column(
            "search_title_zh_hant", sa.TEXT(), nullable=True, comment="JSON array"
        ),
        sa.Column("search_artist_ja", sa.TEXT(), nullable=True, comment="JSON array"),
        sa.Column("search_artist_ko", sa.TEXT(), nullable=True, comment="JSON array"),
        sa.Column(
            "search_artist_zh_hans", sa.TEXT(), nullable=True, comment="JSON array"
        ),
        sa.Column(
            "search_artist_zh_hant", sa.TEXT(), nullable=True, comment="JSON array"
        ),
        sa.Column("source_ja", sa.TEXT(), nullable=True),
        sa.Column("source_ko", sa.TEXT(), nullable=True),
        sa.Column("source_zh_hans", sa.TEXT(), nullable=True),
        sa.Column("source_zh_hant", sa.TEXT(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id"],
            ["songs.id"],
            name="fk_songs_localized_id_songs",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_songs_localized"),
    )
    op.drop_table("aliases")
    op.drop_table("packages")
    op.execute(sa.text("DROP VIEW IF EXISTS bests"))
    op.execute(sa.text("DROP VIEW IF EXISTS calculated"))
    op.execute(sa.text("DROP VIEW IF EXISTS calculated_potential"))
    op.execute(sa.text("DROP VIEW IF EXISTS song_id_names"))

    op.rename_table("scores", "scores_old")
    scores_tbl = op.create_table(
        "scores",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("song_id", sa.TEXT(), nullable=False),
        sa.Column("rating_class", sa.Integer(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("pure", sa.Integer()),
        sa.Column("far", sa.Integer()),
        sa.Column("lost", sa.Integer()),
        sa.Column("date", sa.Integer()),
        sa.Column("max_recall", sa.Integer()),
        sa.Column("modifier", sa.Integer(), comment="0: NORMAL, 1: EASY, 2: HARD"),
        sa.Column(
            "clear_type",
            sa.Integer(),
            comment="0: TRACK LOST, 1: NORMAL CLEAR, 2: FULL RECALL, "
            "3: PURE MEMORY, 4: EASY CLEAR, 5: HARD CLEAR",
        ),
        sa.Column("comment", sa.TEXT()),
    )
    if data_migration:
        conn = op.get_bind()
        query = conn.execute(
            sa.text(
                "SELECT id, song_id, rating_class, score, time, pure, far, lost, max_recall, clear_type "
                "FROM scores_old"
            )
        )
        batch_size = 30

        while True:
            rows = query.fetchmany(batch_size)
            if not rows:
                break

            rows_to_insert = []

            for row in rows:
                result = row._asdict()
                result["date"] = datetime.fromtimestamp(
                    result.pop("time"), tz=timezone.utc
                )

                if threshold_date is not None and result["date"] <= threshold_date:
                    result["date"] = None

                result["date"] = (
                    int(result["date"].timestamp())
                    if result["date"] is not None
                    else None
                )
                rows_to_insert.append(result)

            conn.execute(sa.insert(scores_tbl), rows_to_insert)

    op.drop_table("scores_old")

    op.drop_table("properties", if_exists=True)
    properties_tbl = op.create_table(
        "properties",
        sa.Column("key", sa.TEXT(), nullable=False),
        sa.Column("value", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("key", name="pk_properties"),
    )

    op.execute(sa.insert(properties_tbl).values(key="version", value="4"))


def downgrade() -> None:
    raise NotImplementedError(
        f"Downgrade not supported! ({context.get_context().get_current_revision()})"
    )
