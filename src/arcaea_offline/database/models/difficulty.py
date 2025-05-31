from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    Numeric,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import ModelBase, ReprHelper
from ._types import ForceTimezoneDateTime

if TYPE_CHECKING:
    from .chart_info import ChartInfo
    from .song import Song


class Difficulty(ModelBase, ReprHelper):
    __tablename__ = "difficulty"

    song_id: Mapped[str] = mapped_column(
        ForeignKey("song.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    song: Mapped["Song"] = relationship(back_populates="difficulties")
    localization_entries: Mapped[list["DifficultyLocalization"]] = relationship(
        back_populates="difficulty",
        cascade="all, delete",
        passive_deletes=True,
    )
    chart_info_list: Mapped[list["ChartInfo"]] = relationship(
        back_populates="difficulty",
        cascade="all, delete",
        passive_deletes=True,
    )

    rating_class: Mapped[int] = mapped_column(Integer, primary_key=True)

    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    is_rating_plus: Mapped[bool] = mapped_column(
        Boolean, nullable=False, insert_default=False, server_default=text("0")
    )

    chart_designer: Mapped[Optional[str]] = mapped_column(String)
    jacket_designer: Mapped[Optional[str]] = mapped_column(String)

    has_overriding_audio: Mapped[bool] = mapped_column(
        Boolean, nullable=False, insert_default=False, server_default=text("0")
    )
    has_overriding_jacket: Mapped[bool] = mapped_column(
        Boolean, nullable=False, insert_default=False, server_default=text("0")
    )
    jacket_night: Mapped[Optional[str]] = mapped_column(String)

    title: Mapped[Optional[str]] = mapped_column(String)
    artist: Mapped[Optional[str]] = mapped_column(String)
    bg: Mapped[Optional[str]] = mapped_column(String)
    bg_inverse: Mapped[Optional[str]] = mapped_column(String)
    bpm: Mapped[Optional[str]] = mapped_column(String)
    bpm_base: Mapped[Optional[Decimal]] = mapped_column(Numeric(asdecimal=True))
    added_at: Mapped[Optional[datetime]] = mapped_column(ForceTimezoneDateTime)
    version: Mapped[Optional[str]] = mapped_column(String)
    is_legacy11: Mapped[bool] = mapped_column(
        Boolean, nullable=False, insert_default=False, server_default=text("0")
    )


class DifficultyLocalization(ModelBase, ReprHelper):
    __tablename__ = "difficulty_localization"
    __table_args__ = (
        ForeignKeyConstraint(
            ["song_id", "rating_class"],
            ["difficulty.song_id", "difficulty.rating_class"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )

    difficulty: Mapped["Difficulty"] = relationship(
        back_populates="localization_entries"
    )
    song_id: Mapped[str] = mapped_column(String, primary_key=True)
    rating_class: Mapped[int] = mapped_column(Integer, primary_key=True)

    lang: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String)
