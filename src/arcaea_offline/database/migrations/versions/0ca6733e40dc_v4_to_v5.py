"""v4 to v5

Revision ID: 0ca6733e40dc
Revises: a3f9d48b7de3
Create Date: 2025-05-31 11:38:25.575124

"""

from datetime import datetime, timezone
from typing import Any, Sequence, Union
from uuid import uuid4

import sqlalchemy as sa
from alembic import context, op

from arcaea_offline.database.migrations.legacies.v5 import ForceTimezoneDateTime

# revision identifiers, used by Alembic.
revision: str = "0ca6733e40dc"
down_revision: Union[str, None] = "a3f9d48b7de3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(
    *,
    data_migration: bool = True,
    data_migration_options: Any = None,
) -> None:
    property_tbl = op.create_table(
        "property",
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("key", name=op.f("pk_property")),
    )

    op.create_table(
        "pack",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("section", sa.String(), nullable=True),
        sa.Column(
            "is_world_extend", sa.Boolean(), server_default=sa.text("0"), nullable=False
        ),
        sa.Column("plus_character", sa.Integer(), nullable=True),
        sa.Column("append_parent_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["append_parent_id"],
            ["pack.id"],
            name=op.f("fk_pack_append_parent_id_pack"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_pack")),
    )
    with op.batch_alter_table("pack", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_pack_name"), ["name"], unique=False)

    op.create_table(
        "pack_localization",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("lang", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id"],
            ["pack.id"],
            name=op.f("fk_pack_localization_id_pack"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", "lang", name=op.f("pk_pack_localization")),
    )
    op.create_table(
        "song",
        sa.Column("pack_id", sa.String(), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("idx", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("artist", sa.String(), nullable=True),
        sa.Column(
            "is_deleted", sa.Boolean(), server_default=sa.text("0"), nullable=False
        ),
        sa.Column("added_at", ForceTimezoneDateTime(), nullable=False),
        sa.Column("version", sa.String(), nullable=True),
        sa.Column("bpm", sa.String(), nullable=True),
        sa.Column("bpm_base", sa.Numeric(), nullable=True),
        sa.Column(
            "is_remote", sa.Boolean(), server_default=sa.text("0"), nullable=False
        ),
        sa.Column(
            "is_unlockable_in_world",
            sa.Boolean(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "is_beyond_unlock_state_local",
            sa.Boolean(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column("purchase", sa.String(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("side", sa.Integer(), nullable=True),
        sa.Column("bg", sa.String(), nullable=True),
        sa.Column("bg_inverse", sa.String(), nullable=True),
        sa.Column("bg_day", sa.String(), nullable=True),
        sa.Column("bg_night", sa.String(), nullable=True),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("source_copyright", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["pack_id"],
            ["pack.id"],
            name=op.f("fk_song_pack_id_pack"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_song")),
    )
    with op.batch_alter_table("song", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_song_added_at"), ["added_at"], unique=False
        )
        batch_op.create_index(batch_op.f("ix_song_artist"), ["artist"], unique=False)
        batch_op.create_index(batch_op.f("ix_song_title"), ["title"], unique=False)

    op.create_table(
        "difficulty",
        sa.Column("song_id", sa.String(), nullable=False),
        sa.Column("rating_class", sa.Integer(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column(
            "is_rating_plus", sa.Boolean(), server_default=sa.text("0"), nullable=False
        ),
        sa.Column("chart_designer", sa.String(), nullable=True),
        sa.Column("jacket_designer", sa.String(), nullable=True),
        sa.Column(
            "has_overriding_audio",
            sa.Boolean(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "has_overriding_jacket",
            sa.Boolean(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column("jacket_night", sa.String(), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("artist", sa.String(), nullable=True),
        sa.Column("bg", sa.String(), nullable=True),
        sa.Column("bg_inverse", sa.String(), nullable=True),
        sa.Column("bpm", sa.String(), nullable=True),
        sa.Column("bpm_base", sa.Numeric(), nullable=True),
        sa.Column("added_at", ForceTimezoneDateTime(), nullable=True),
        sa.Column("version", sa.String(), nullable=True),
        sa.Column(
            "is_legacy11", sa.Boolean(), server_default=sa.text("0"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["song_id"],
            ["song.id"],
            name=op.f("fk_difficulty_song_id_song"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("song_id", "rating_class", name=op.f("pk_difficulty")),
    )
    op.create_table(
        "song_localization",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("lang", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column(
            "has_jacket", sa.Boolean(), server_default=sa.text("0"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["song.id"],
            name=op.f("fk_song_localization_id_song"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", "lang", name=op.f("pk_song_localization")),
    )
    op.create_table(
        "chart_info",
        sa.Column("song_id", sa.String(), nullable=False),
        sa.Column("rating_class", sa.Integer(), nullable=False),
        sa.Column("constant", sa.Numeric(), nullable=False),
        sa.Column("notes", sa.Integer(), nullable=False),
        sa.Column(
            "added_at",
            ForceTimezoneDateTime(),
            nullable=False,
        ),
        sa.Column("version", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["song_id", "rating_class"],
            ["difficulty.song_id", "difficulty.rating_class"],
            name=op.f("fk_chart_info_song_id_difficulty"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "song_id", "rating_class", "added_at", name=op.f("pk_chart_info")
        ),
    )
    op.create_table(
        "difficulty_localization",
        sa.Column("song_id", sa.String(), nullable=False),
        sa.Column("rating_class", sa.Integer(), nullable=False),
        sa.Column("lang", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["song_id", "rating_class"],
            ["difficulty.song_id", "difficulty.rating_class"],
            name=op.f("fk_difficulty_localization_song_id_difficulty"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "song_id", "rating_class", "lang", name=op.f("pk_difficulty_localization")
        ),
    )

    op.drop_table("properties")
    op.drop_table("packs")
    op.drop_table("packs_localized")
    op.drop_table("difficulties")
    op.drop_table("songs")
    op.drop_table("songs_localized")
    op.drop_table("charts")
    op.drop_table("charts_info")
    op.drop_table("difficulties_localized")

    op.rename_table("scores", "scores_old")
    play_result_tbl = op.create_table(
        "play_result",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", sa.Uuid(), nullable=False),
        sa.Column("song_id", sa.String(), nullable=False),
        sa.Column("rating_class", sa.Integer(), nullable=False),
        sa.Column("played_at", ForceTimezoneDateTime(), nullable=True),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("pure", sa.Integer(), nullable=True),
        sa.Column("pure_early", sa.Integer(), nullable=True),
        sa.Column("pure_late", sa.Integer(), nullable=True),
        sa.Column("far", sa.Integer(), nullable=True),
        sa.Column("far_early", sa.Integer(), nullable=True),
        sa.Column("far_late", sa.Integer(), nullable=True),
        sa.Column("lost", sa.Integer(), nullable=True),
        sa.Column("max_recall", sa.Integer(), nullable=True),
        sa.Column("clear_type", sa.Integer(), nullable=True),
        sa.Column("modifier", sa.Integer(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_play_result")),
        sa.UniqueConstraint("uuid", name=op.f("uq_play_result_uuid")),
    )

    if data_migration:
        conn = op.get_bind()
        query = conn.execute(
            sa.text(
                "SELECT id, song_id, rating_class, score, pure, far, lost, "
                " `date`, max_recall, modifier, clear_type, comment "
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

                date = result.pop("date")
                result["uuid"] = uuid4()
                result["played_at"] = (
                    datetime.fromtimestamp(date, tz=timezone.utc)
                    if date is not None
                    else None
                )
                rows_to_insert.append(result)

            conn.execute(sa.insert(play_result_tbl), rows_to_insert)

    op.drop_table("scores_old")

    op.execute(sa.insert(property_tbl).values(key="version", value="5"))


def downgrade() -> None:
    raise NotImplementedError(
        f"Downgrade not supported! ({context.get_context().get_current_revision()})"
    )

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "difficulties_localized",
        sa.Column("song_id", sa.TEXT(), nullable=False),
        sa.Column("rating_class", sa.INTEGER(), nullable=False),
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
            name=op.f("fk_difficulties_localized_rating_class_difficulties"),
        ),
        sa.ForeignKeyConstraint(
            ["song_id"],
            ["difficulties.song_id"],
            name=op.f("fk_difficulties_localized_song_id_difficulties"),
        ),
        sa.PrimaryKeyConstraint(
            "song_id", "rating_class", name=op.f("pk_difficulties_localized")
        ),
    )
    op.create_table(
        "charts_info",
        sa.Column("song_id", sa.TEXT(), nullable=False),
        sa.Column("rating_class", sa.INTEGER(), nullable=False),
        sa.Column("constant", sa.INTEGER(), nullable=False),
        sa.Column("notes", sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(
            ["rating_class"],
            ["difficulties.rating_class"],
            name=op.f("fk_charts_info_rating_class_difficulties"),
        ),
        sa.ForeignKeyConstraint(
            ["song_id"],
            ["difficulties.song_id"],
            name=op.f("fk_charts_info_song_id_difficulties"),
        ),
        sa.PrimaryKeyConstraint("song_id", "rating_class", name=op.f("pk_charts_info")),
    )
    op.create_table(
        "charts",
        sa.Column("song_id", sa.TEXT(), nullable=False),
        sa.Column("rating_class", sa.INTEGER(), nullable=False),
        sa.Column("name_en", sa.TEXT(), nullable=False),
        sa.Column("name_jp", sa.TEXT(), nullable=True),
        sa.Column("artist", sa.TEXT(), nullable=False),
        sa.Column("bpm", sa.TEXT(), nullable=False),
        sa.Column("bpm_base", sa.REAL(), nullable=False),
        sa.Column("package_id", sa.TEXT(), nullable=False),
        sa.Column("time", sa.INTEGER(), nullable=True),
        sa.Column("side", sa.INTEGER(), nullable=False),
        sa.Column("world_unlock", sa.BOOLEAN(), nullable=False),
        sa.Column("remote_download", sa.BOOLEAN(), nullable=True),
        sa.Column("bg", sa.TEXT(), nullable=False),
        sa.Column("date", sa.INTEGER(), nullable=False),
        sa.Column("version", sa.TEXT(), nullable=False),
        sa.Column("difficulty", sa.INTEGER(), nullable=False),
        sa.Column("rating", sa.INTEGER(), nullable=False),
        sa.Column("note", sa.INTEGER(), nullable=False),
        sa.Column("chart_designer", sa.TEXT(), nullable=True),
        sa.Column("jacket_designer", sa.TEXT(), nullable=True),
        sa.Column("jacket_override", sa.BOOLEAN(), nullable=False),
        sa.Column("audio_override", sa.BOOLEAN(), nullable=False),
        sa.PrimaryKeyConstraint("song_id", "rating_class"),
    )
    op.create_table(
        "songs_localized",
        sa.Column("id", sa.TEXT(), nullable=False),
        sa.Column("title_ja", sa.TEXT(), nullable=True),
        sa.Column("title_ko", sa.TEXT(), nullable=True),
        sa.Column("title_zh_hans", sa.TEXT(), nullable=True),
        sa.Column("title_zh_hant", sa.TEXT(), nullable=True),
        sa.Column("search_title_ja", sa.TEXT(), nullable=True),
        sa.Column("search_title_ko", sa.TEXT(), nullable=True),
        sa.Column("search_title_zh_hans", sa.TEXT(), nullable=True),
        sa.Column("search_title_zh_hant", sa.TEXT(), nullable=True),
        sa.Column("search_artist_ja", sa.TEXT(), nullable=True),
        sa.Column("search_artist_ko", sa.TEXT(), nullable=True),
        sa.Column("search_artist_zh_hans", sa.TEXT(), nullable=True),
        sa.Column("search_artist_zh_hant", sa.TEXT(), nullable=True),
        sa.Column("source_ja", sa.TEXT(), nullable=True),
        sa.Column("source_ko", sa.TEXT(), nullable=True),
        sa.Column("source_zh_hans", sa.TEXT(), nullable=True),
        sa.Column("source_zh_hant", sa.TEXT(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id"], ["songs.id"], name=op.f("fk_songs_localized_id_songs")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_songs_localized")),
    )
    op.create_table(
        "packs",
        sa.Column("id", sa.TEXT(), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="fk_packs"),
    )
    op.create_table(
        "properties",
        sa.Column("key", sa.TEXT(), nullable=False),
        sa.Column("value", sa.TEXT(), nullable=False),
        sa.UniqueConstraint("key"),
    )
    op.create_table(
        "songs",
        sa.Column("idx", sa.INTEGER(), nullable=False),
        sa.Column("id", sa.TEXT(), nullable=False),
        sa.Column("title", sa.TEXT(), nullable=False),
        sa.Column("artist", sa.TEXT(), nullable=False),
        sa.Column("set", sa.TEXT(), nullable=False),
        sa.Column("bpm", sa.TEXT(), nullable=True),
        sa.Column("bpm_base", sa.FLOAT(), nullable=True),
        sa.Column("audio_preview", sa.INTEGER(), nullable=True),
        sa.Column("audio_preview_end", sa.INTEGER(), nullable=True),
        sa.Column("side", sa.INTEGER(), nullable=True),
        sa.Column("version", sa.TEXT(), nullable=True),
        sa.Column("date", sa.INTEGER(), nullable=True),
        sa.Column("bg", sa.TEXT(), nullable=True),
        sa.Column("bg_inverse", sa.TEXT(), nullable=True),
        sa.Column("bg_day", sa.TEXT(), nullable=True),
        sa.Column("bg_night", sa.TEXT(), nullable=True),
        sa.Column("source", sa.TEXT(), nullable=True),
        sa.Column("source_copyright", sa.TEXT(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("songs")),
    )
    op.create_table(
        "difficulties",
        sa.Column("song_id", sa.TEXT(), nullable=False),
        sa.Column("rating_class", sa.INTEGER(), nullable=False),
        sa.Column("rating", sa.INTEGER(), nullable=False),
        sa.Column("rating_plus", sa.BOOLEAN(), nullable=False),
        sa.Column("chart_designer", sa.TEXT(), nullable=True),
        sa.Column("jacket_desginer", sa.TEXT(), nullable=True),
        sa.Column("audio_override", sa.BOOLEAN(), nullable=False),
        sa.Column("jacket_override", sa.BOOLEAN(), nullable=False),
        sa.Column("jacket_night", sa.TEXT(), nullable=True),
        sa.Column("title", sa.TEXT(), nullable=True),
        sa.Column("artist", sa.TEXT(), nullable=True),
        sa.Column("bg", sa.TEXT(), nullable=True),
        sa.Column("bg_inverse", sa.TEXT(), nullable=True),
        sa.Column("bpm", sa.TEXT(), nullable=True),
        sa.Column("bpm_base", sa.FLOAT(), nullable=True),
        sa.Column("version", sa.TEXT(), nullable=True),
        sa.Column("date", sa.INTEGER(), nullable=True),
        sa.PrimaryKeyConstraint(
            "song_id", "rating_class", name=op.f("pk_difficulties")
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
            ["id"], ["packs.id"], name=op.f("fk_packs_localized_id_packs")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_packs_localized")),
    )
    op.create_table(
        "scores",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("song_id", sa.TEXT(), nullable=False),
        sa.Column("rating_class", sa.INTEGER(), nullable=False),
        sa.Column("score", sa.INTEGER(), nullable=False),
        sa.Column("pure", sa.INTEGER(), nullable=True),
        sa.Column("far", sa.INTEGER(), nullable=True),
        sa.Column("lost", sa.INTEGER(), nullable=True),
        sa.Column("date", sa.INTEGER(), nullable=True),
        sa.Column("max_recall", sa.INTEGER(), nullable=True),
        sa.Column("modifier", sa.INTEGER(), nullable=True),
        sa.Column("clear_type", sa.INTEGER(), nullable=True),
        sa.Column("comment", sa.TEXT(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("difficulty_localization")
    op.drop_table("chart_info")
    op.drop_table("song_localization")
    op.drop_table("difficulty")
    with op.batch_alter_table("song", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_song_title"))
        batch_op.drop_index(batch_op.f("ix_song_artist"))
        batch_op.drop_index(batch_op.f("ix_song_added_at"))

    op.drop_table("song")
    op.drop_table("pack_localization")
    op.drop_table("property")
    op.drop_table("play_result")
    with op.batch_alter_table("pack", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_pack_name"))

    op.drop_table("pack")
    # ### end Alembic commands ###
