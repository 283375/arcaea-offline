from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from arcaea_offline.utils import Version

from ._base import ModelBase, ReprHelper
from ._types import ForceTimezoneDateTime

if TYPE_CHECKING:
    from .difficulty import Difficulty
    from .pack import Pack


class Song(ModelBase, ReprHelper):
    __tablename__ = "song"

    pack_id: Mapped[str] = mapped_column(
        ForeignKey("pack.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    pack: Mapped["Pack"] = relationship(back_populates="songs")
    difficulties: Mapped[list["Difficulty"]] = relationship(
        back_populates="song",
        cascade="all, delete",
        passive_deletes=True,
    )
    localized_entries: Mapped[list["SongLocalization"]] = relationship(
        back_populates="song",
        cascade="all, delete",
        passive_deletes=True,
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    idx: Mapped[Optional[int]] = mapped_column(Integer)
    title: Mapped[Optional[str]] = mapped_column(String, index=True)
    artist: Mapped[Optional[str]] = mapped_column(String, index=True)
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, insert_default=False, server_default=text("0")
    )

    added_at: Mapped[datetime] = mapped_column(
        ForceTimezoneDateTime, nullable=False, index=True
    )
    version: Mapped[Optional[Version]]

    bpm: Mapped[Optional[str]] = mapped_column(String)
    bpm_base: Mapped[Optional[Decimal]] = mapped_column(Numeric(asdecimal=True))
    is_remote: Mapped[bool] = mapped_column(
        Boolean, nullable=False, insert_default=False, server_default=text("0")
    )
    is_unlockable_in_world: Mapped[bool] = mapped_column(
        Boolean, nullable=False, insert_default=False, server_default=text("0")
    )
    is_beyond_unlock_state_local: Mapped[bool] = mapped_column(
        Boolean, nullable=False, insert_default=False, server_default=text("0")
    )
    purchase: Mapped[Optional[str]] = mapped_column(String)
    category: Mapped[Optional[str]] = mapped_column(String)

    side: Mapped[Optional[int]] = mapped_column(Integer)
    bg: Mapped[Optional[str]] = mapped_column(String)
    bg_inverse: Mapped[Optional[str]] = mapped_column(String)
    bg_day: Mapped[Optional[str]] = mapped_column(String)
    bg_night: Mapped[Optional[str]] = mapped_column(String)

    source: Mapped[Optional[str]] = mapped_column(String)
    source_copyright: Mapped[Optional[str]] = mapped_column(String)


class SongLocalization(ModelBase, ReprHelper):
    __tablename__ = "song_localization"

    song: Mapped["Song"] = relationship(back_populates="localized_entries")
    id: Mapped[str] = mapped_column(
        ForeignKey("song.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )

    lang: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String)
    source: Mapped[Optional[str]] = mapped_column(String)
    has_jacket: Mapped[bool] = mapped_column(
        Boolean, nullable=False, insert_default=False, server_default=text("0")
    )
