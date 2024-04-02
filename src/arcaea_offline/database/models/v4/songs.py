# pylint: disable=too-few-public-methods, duplicate-code

from typing import Optional

from sqlalchemy import TEXT, ForeignKey, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy_utils import create_view

from .common import ReprHelper

__all__ = [
    "SongsBase",
    "Pack",
    "PackLocalized",
    "Song",
    "SongLocalized",
    "Difficulty",
    "DifficultyLocalized",
    "ChartInfo",
    "SongsViewBase",
    "Chart",
]


class SongsBase(DeclarativeBase, ReprHelper):
    pass


class Pack(SongsBase):
    __tablename__ = "packs"

    id: Mapped[str] = mapped_column(TEXT(), primary_key=True)
    name: Mapped[str] = mapped_column(TEXT())
    description: Mapped[Optional[str]] = mapped_column(TEXT())


class PackLocalized(SongsBase):
    __tablename__ = "packs_localized"

    id: Mapped[str] = mapped_column(ForeignKey("packs.id"), primary_key=True)
    name_ja: Mapped[Optional[str]] = mapped_column(TEXT())
    name_ko: Mapped[Optional[str]] = mapped_column(TEXT())
    name_zh_hans: Mapped[Optional[str]] = mapped_column(TEXT())
    name_zh_hant: Mapped[Optional[str]] = mapped_column(TEXT())
    description_ja: Mapped[Optional[str]] = mapped_column(TEXT())
    description_ko: Mapped[Optional[str]] = mapped_column(TEXT())
    description_zh_hans: Mapped[Optional[str]] = mapped_column(TEXT())
    description_zh_hant: Mapped[Optional[str]] = mapped_column(TEXT())


class Song(SongsBase):
    __tablename__ = "songs"

    idx: Mapped[int]
    id: Mapped[str] = mapped_column(TEXT(), primary_key=True)
    title: Mapped[str] = mapped_column(TEXT())
    artist: Mapped[str] = mapped_column(TEXT())
    set: Mapped[str] = mapped_column(TEXT())
    bpm: Mapped[Optional[str]] = mapped_column(TEXT())
    bpm_base: Mapped[Optional[float]]
    audio_preview: Mapped[Optional[int]]
    audio_preview_end: Mapped[Optional[int]]
    side: Mapped[Optional[int]]
    version: Mapped[Optional[str]] = mapped_column(TEXT())
    date: Mapped[Optional[int]]
    bg: Mapped[Optional[str]] = mapped_column(TEXT())
    bg_inverse: Mapped[Optional[str]] = mapped_column(TEXT())
    bg_day: Mapped[Optional[str]] = mapped_column(TEXT())
    bg_night: Mapped[Optional[str]] = mapped_column(TEXT())
    source: Mapped[Optional[str]] = mapped_column(TEXT())
    source_copyright: Mapped[Optional[str]] = mapped_column(TEXT())


class SongLocalized(SongsBase):
    __tablename__ = "songs_localized"

    id: Mapped[str] = mapped_column(ForeignKey("songs.id"), primary_key=True)
    title_ja: Mapped[Optional[str]] = mapped_column(TEXT())
    title_ko: Mapped[Optional[str]] = mapped_column(TEXT())
    title_zh_hans: Mapped[Optional[str]] = mapped_column(TEXT())
    title_zh_hant: Mapped[Optional[str]] = mapped_column(TEXT())
    search_title_ja: Mapped[Optional[str]] = mapped_column(TEXT(), comment="JSON array")
    search_title_ko: Mapped[Optional[str]] = mapped_column(TEXT(), comment="JSON array")
    search_title_zh_hans: Mapped[Optional[str]] = mapped_column(
        TEXT(), comment="JSON array"
    )
    search_title_zh_hant: Mapped[Optional[str]] = mapped_column(
        TEXT(), comment="JSON array"
    )
    search_artist_ja: Mapped[Optional[str]] = mapped_column(
        TEXT(), comment="JSON array"
    )
    search_artist_ko: Mapped[Optional[str]] = mapped_column(
        TEXT(), comment="JSON array"
    )
    search_artist_zh_hans: Mapped[Optional[str]] = mapped_column(
        TEXT(), comment="JSON array"
    )
    search_artist_zh_hant: Mapped[Optional[str]] = mapped_column(
        TEXT(), comment="JSON array"
    )
    source_ja: Mapped[Optional[str]] = mapped_column(TEXT())
    source_ko: Mapped[Optional[str]] = mapped_column(TEXT())
    source_zh_hans: Mapped[Optional[str]] = mapped_column(TEXT())
    source_zh_hant: Mapped[Optional[str]] = mapped_column(TEXT())


class Difficulty(SongsBase):
    __tablename__ = "difficulties"

    song_id: Mapped[str] = mapped_column(TEXT(), primary_key=True)
    rating_class: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[int]
    rating_plus: Mapped[bool]
    chart_designer: Mapped[Optional[str]] = mapped_column(TEXT())
    jacket_desginer: Mapped[Optional[str]] = mapped_column(TEXT())
    audio_override: Mapped[bool]
    jacket_override: Mapped[bool]
    jacket_night: Mapped[Optional[str]] = mapped_column(TEXT())
    title: Mapped[Optional[str]] = mapped_column(TEXT())
    artist: Mapped[Optional[str]] = mapped_column(TEXT())
    bg: Mapped[Optional[str]] = mapped_column(TEXT())
    bg_inverse: Mapped[Optional[str]] = mapped_column(TEXT())
    bpm: Mapped[Optional[str]] = mapped_column(TEXT())
    bpm_base: Mapped[Optional[float]]
    version: Mapped[Optional[str]] = mapped_column(TEXT())
    date: Mapped[Optional[int]]


class DifficultyLocalized(SongsBase):
    __tablename__ = "difficulties_localized"

    song_id: Mapped[str] = mapped_column(
        ForeignKey("difficulties.song_id"), primary_key=True
    )
    rating_class: Mapped[str] = mapped_column(
        ForeignKey("difficulties.rating_class"), primary_key=True
    )
    title_ja: Mapped[Optional[str]] = mapped_column(TEXT())
    title_ko: Mapped[Optional[str]] = mapped_column(TEXT())
    title_zh_hans: Mapped[Optional[str]] = mapped_column(TEXT())
    title_zh_hant: Mapped[Optional[str]] = mapped_column(TEXT())
    artist_ja: Mapped[Optional[str]] = mapped_column(TEXT())
    artist_ko: Mapped[Optional[str]] = mapped_column(TEXT())
    artist_zh_hans: Mapped[Optional[str]] = mapped_column(TEXT())
    artist_zh_hant: Mapped[Optional[str]] = mapped_column(TEXT())


class ChartInfo(SongsBase):
    __tablename__ = "charts_info"

    song_id: Mapped[str] = mapped_column(
        ForeignKey("difficulties.song_id"), primary_key=True
    )
    rating_class: Mapped[str] = mapped_column(
        ForeignKey("difficulties.rating_class"), primary_key=True
    )
    constant: Mapped[int] = mapped_column(
        comment="real_constant * 10. For example, Crimson Throne [FTR] is 10.4, then store 104."
    )
    notes: Mapped[Optional[int]]


class SongsViewBase(DeclarativeBase, ReprHelper):
    pass


class Chart(SongsViewBase):
    __tablename__ = "charts"

    song_idx: Mapped[int]
    song_id: Mapped[str]
    rating_class: Mapped[int]
    rating: Mapped[int]
    rating_plus: Mapped[bool]
    title: Mapped[str]
    artist: Mapped[str]
    set: Mapped[str]
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
            Song.set,
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
        metadata=SongsViewBase.metadata,
        cascade_on_drop=False,
    )
