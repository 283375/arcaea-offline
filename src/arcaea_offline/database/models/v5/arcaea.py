from typing import List, Optional

from sqlalchemy import ForeignKey, and_, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import create_view

from arcaea_offline.constants.enums import ArcaeaRatingClass, ArcaeaSongSide

from .base import ModelsV5Base, ModelsV5ViewBase, ReprHelper

__all__ = [
    "Chart",
    "ChartInfo",
    "Difficulty",
    "DifficultyLocalized",
    "Pack",
    "PackLocalized",
    "Song",
    "SongLocalized",
]


class Pack(ModelsV5Base, ReprHelper):
    __tablename__ = "packs"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]

    songs: Mapped[List["Song"]] = relationship(back_populates="pack", viewonly=True)
    localized_objects: Mapped[List["PackLocalized"]] = relationship(
        back_populates="parent", viewonly=True
    )


class PackLocalized(ModelsV5Base, ReprHelper):
    __tablename__ = "packs_localized"

    pkid: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[str] = mapped_column(
        ForeignKey(Pack.id, onupdate="CASCADE", ondelete="NO ACTION")
    )
    lang: Mapped[str]
    name: Mapped[Optional[str]]
    description: Mapped[Optional[str]]

    parent: Mapped[Pack] = relationship(viewonly=True)


class Song(ModelsV5Base, ReprHelper):
    __tablename__ = "songs"

    idx: Mapped[int]
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    artist: Mapped[str]
    pack_id: Mapped[str] = mapped_column(
        ForeignKey(Pack.id, onupdate="CASCADE", ondelete="NO ACTION")
    )
    bpm: Mapped[Optional[str]]
    bpm_base: Mapped[Optional[float]]
    audio_preview: Mapped[Optional[int]]
    audio_preview_end: Mapped[Optional[int]]
    side: Mapped[Optional[ArcaeaSongSide]]
    version: Mapped[Optional[str]]
    date: Mapped[Optional[int]]
    bg: Mapped[Optional[str]]
    bg_inverse: Mapped[Optional[str]]
    bg_day: Mapped[Optional[str]]
    bg_night: Mapped[Optional[str]]
    source: Mapped[Optional[str]]
    source_copyright: Mapped[Optional[str]]

    pack: Mapped[Pack] = relationship(viewonly=True)
    difficulties: Mapped[List["Difficulty"]] = relationship(
        back_populates="song", viewonly=True
    )
    localized_objects: Mapped[List["SongLocalized"]] = relationship(
        back_populates="parent", viewonly=True
    )

    @property
    def charts_info(self):
        return [d.chart_info for d in self.difficulties if d.chart_info is not None]


class SongLocalized(ModelsV5Base, ReprHelper):
    __tablename__ = "songs_localized"

    pkid: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[str] = mapped_column(
        ForeignKey(Song.id, onupdate="CASCADE", ondelete="NO ACTION")
    )
    lang: Mapped[str]
    title: Mapped[Optional[str]]
    source: Mapped[Optional[str]]

    parent: Mapped[Song] = relationship(
        back_populates="localized_objects", viewonly=True
    )


class SongSearchWord(ModelsV5Base, ReprHelper):
    __tablename__ = "songs_search_words"

    pkid: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[str] = mapped_column(
        ForeignKey(Song.id, onupdate="CASCADE", ondelete="NO ACTION")
    )
    lang: Mapped[str]
    type: Mapped[int] = mapped_column(comment="1: title, 2: artist")
    value: Mapped[str]


class Difficulty(ModelsV5Base, ReprHelper):
    __tablename__ = "difficulties"

    song_id: Mapped[str] = mapped_column(
        ForeignKey(Song.id, onupdate="CASCADE", ondelete="NO ACTION"),
        primary_key=True,
    )
    rating_class: Mapped[ArcaeaRatingClass] = mapped_column(primary_key=True)
    rating: Mapped[int]
    rating_plus: Mapped[bool]
    chart_designer: Mapped[Optional[str]]
    jacket_desginer: Mapped[Optional[str]]
    audio_override: Mapped[bool] = mapped_column(default=False)
    jacket_override: Mapped[bool] = mapped_column(default=False)
    jacket_night: Mapped[Optional[str]]
    title: Mapped[Optional[str]]
    artist: Mapped[Optional[str]]
    bg: Mapped[Optional[str]]
    bg_inverse: Mapped[Optional[str]]
    bpm: Mapped[Optional[str]]
    bpm_base: Mapped[Optional[float]]
    version: Mapped[Optional[str]]
    date: Mapped[Optional[int]]

    song: Mapped[Song] = relationship(back_populates="difficulties", viewonly=True)
    chart_info: Mapped[Optional["ChartInfo"]] = relationship(
        primaryjoin=(
            "and_(Difficulty.song_id==ChartInfo.song_id, "
            "Difficulty.rating_class==ChartInfo.rating_class)"
        ),
        viewonly=True,
    )
    localized_objects: Mapped[List["DifficultyLocalized"]] = relationship(
        primaryjoin=(
            "and_(Difficulty.song_id==DifficultyLocalized.song_id, "
            "Difficulty.rating_class==DifficultyLocalized.rating_class)"
        ),
        viewonly=True,
    )


class DifficultyLocalized(ModelsV5Base, ReprHelper):
    __tablename__ = "difficulties_localized"

    pkid: Mapped[int] = mapped_column(primary_key=True)
    song_id: Mapped[str] = mapped_column(
        ForeignKey(Difficulty.song_id, onupdate="CASCADE", ondelete="NO ACTION")
    )
    rating_class: Mapped[ArcaeaRatingClass] = mapped_column(
        ForeignKey(Difficulty.rating_class, onupdate="CASCADE", ondelete="NO ACTION")
    )
    lang: Mapped[str]
    title: Mapped[Optional[str]]
    artist: Mapped[Optional[str]]

    parent: Mapped[Difficulty] = relationship(
        primaryjoin=and_(
            Difficulty.song_id == song_id, Difficulty.rating_class == rating_class
        ),
        viewonly=True,
    )


class ChartInfo(ModelsV5Base, ReprHelper):
    __tablename__ = "charts_info"

    song_id: Mapped[str] = mapped_column(
        ForeignKey(Difficulty.song_id, onupdate="CASCADE", ondelete="NO ACTION"),
        primary_key=True,
    )
    rating_class: Mapped[ArcaeaRatingClass] = mapped_column(
        ForeignKey(Difficulty.rating_class, onupdate="CASCADE", ondelete="NO ACTION"),
        primary_key=True,
    )
    constant: Mapped[int] = mapped_column(
        comment="real_constant * 10. For example, Crimson Throne [FTR] is 10.4, then store 104."
    )
    notes: Mapped[Optional[int]]

    difficulty: Mapped[Difficulty] = relationship(
        primaryjoin=and_(
            Difficulty.song_id == song_id, Difficulty.rating_class == rating_class
        ),
        viewonly=True,
    )


class Chart(ModelsV5ViewBase, ReprHelper):
    __tablename__ = "charts"

    song_idx: Mapped[int]
    song_id: Mapped[str]
    rating_class: Mapped[ArcaeaRatingClass]
    rating: Mapped[int]
    rating_plus: Mapped[bool]
    title: Mapped[str]
    artist: Mapped[str]
    pack_id: Mapped[str]
    bpm: Mapped[Optional[str]]
    bpm_base: Mapped[Optional[float]]
    audio_preview: Mapped[Optional[int]]
    audio_preview_end: Mapped[Optional[int]]
    side: Mapped[Optional[int]]
    version: Mapped[Optional[str]]
    date: Mapped[Optional[int]]
    bg: Mapped[Optional[str]]
    bg_inverse: Mapped[Optional[str]]
    bg_day: Mapped[Optional[str]]
    bg_night: Mapped[Optional[str]]
    source: Mapped[Optional[str]]
    source_copyright: Mapped[Optional[str]]
    chart_designer: Mapped[Optional[str]]
    jacket_desginer: Mapped[Optional[str]]
    audio_override: Mapped[bool]
    jacket_override: Mapped[bool]
    jacket_night: Mapped[Optional[str]]
    constant: Mapped[int]
    notes: Mapped[Optional[int]]

    __table__ = create_view(
        name=__tablename__,
        selectable=select(
            Song.idx.label("song_idx"),
            Difficulty.song_id,
            Difficulty.rating_class,
            Difficulty.rating,
            Difficulty.rating_plus,
            func.coalesce(Difficulty.title, Song.title).label("title"),
            func.coalesce(Difficulty.artist, Song.artist).label("artist"),
            Song.pack_id,
            func.coalesce(Difficulty.bpm, Song.bpm).label("bpm"),
            func.coalesce(Difficulty.bpm_base, Song.bpm_base).label("bpm_base"),
            Song.audio_preview,
            Song.audio_preview_end,
            Song.side,
            func.coalesce(Difficulty.version, Song.version).label("version"),
            func.coalesce(Difficulty.date, Song.date).label("date"),
            func.coalesce(Difficulty.bg, Song.bg).label("bg"),
            func.coalesce(Difficulty.bg_inverse, Song.bg_inverse).label("bg_inverse"),
            Song.bg_day,
            Song.bg_night,
            Song.source,
            Song.source_copyright,
            Difficulty.chart_designer,
            Difficulty.jacket_desginer,
            Difficulty.audio_override,
            Difficulty.jacket_override,
            Difficulty.jacket_night,
            ChartInfo.constant,
            ChartInfo.notes,
        )
        .select_from(Difficulty)
        .join(
            ChartInfo,
            (Difficulty.song_id == ChartInfo.song_id)
            & (Difficulty.rating_class == ChartInfo.rating_class),
        )
        .join(Song, Difficulty.song_id == Song.id),
        metadata=ModelsV5ViewBase.metadata,
        cascade_on_drop=False,
    )
