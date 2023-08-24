from typing import Optional

from sqlalchemy import TEXT, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class SongsBase(DeclarativeBase):
    pass


class Property(SongsBase):
    __tablename__ = "property"

    id: Mapped[str] = mapped_column(TEXT(), primary_key=True)
    value: Mapped[str] = mapped_column(TEXT())


class Pack(SongsBase):
    __tablename__ = "pack"

    id: Mapped[str] = mapped_column(TEXT(), primary_key=True)
    name: Mapped[str] = mapped_column(TEXT())
    description: Mapped[Optional[str]] = mapped_column(TEXT())


class PackLocalized(SongsBase):
    __tablename__ = "pack_localized"

    id: Mapped[str] = mapped_column(ForeignKey("pack.id"), primary_key=True)
    name_ja: Mapped[Optional[str]] = mapped_column(TEXT())
    name_ko: Mapped[Optional[str]] = mapped_column(TEXT())
    name_zh_hans: Mapped[Optional[str]] = mapped_column(TEXT())
    name_zh_hant: Mapped[Optional[str]] = mapped_column(TEXT())
    description_ja: Mapped[Optional[str]] = mapped_column(TEXT())
    description_ko: Mapped[Optional[str]] = mapped_column(TEXT())
    description_zh_hans: Mapped[Optional[str]] = mapped_column(TEXT())
    description_zh_hant: Mapped[Optional[str]] = mapped_column(TEXT())


class Song(SongsBase):
    __tablename__ = "song"

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
    __tablename__ = "song_localized"

    id: Mapped[str] = mapped_column(ForeignKey("song.id"), primary_key=True)
    title_ja: Mapped[Optional[str]] = mapped_column(TEXT())
    title_ko: Mapped[Optional[str]] = mapped_column(TEXT())
    title_zh_hans: Mapped[Optional[str]] = mapped_column(TEXT())
    title_zh_hant: Mapped[Optional[str]] = mapped_column(TEXT())
    search_title_ja: Mapped[Optional[str]] = mapped_column(TEXT(), comment="json")
    search_title_ko: Mapped[Optional[str]] = mapped_column(TEXT(), comment="json")
    search_title_zh_hans: Mapped[Optional[str]] = mapped_column(TEXT(), comment="json")
    search_title_zh_hant: Mapped[Optional[str]] = mapped_column(TEXT(), comment="json")
    search_artist_ja: Mapped[Optional[str]] = mapped_column(TEXT(), comment="json")
    search_artist_ko: Mapped[Optional[str]] = mapped_column(TEXT(), comment="json")
    search_artist_zh_hans: Mapped[Optional[str]] = mapped_column(TEXT(), comment="json")
    search_artist_zh_hant: Mapped[Optional[str]] = mapped_column(TEXT(), comment="json")
    source_ja: Mapped[Optional[str]] = mapped_column(TEXT())
    source_ko: Mapped[Optional[str]] = mapped_column(TEXT())
    source_zh_hans: Mapped[Optional[str]] = mapped_column(TEXT())
    source_zh_hant: Mapped[Optional[str]] = mapped_column(TEXT())


class Chart(SongsBase):
    __tablename__ = "chart"

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


class ChartLocalized(SongsBase):
    __tablename__ = "chart_localized"

    song_id: Mapped[str] = mapped_column(ForeignKey("chart.song_id"), primary_key=True)
    rating_class: Mapped[str] = mapped_column(
        ForeignKey("chart.rating_class"), primary_key=True
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
    __tablename__ = "chart_info"

    song_id: Mapped[str] = mapped_column(ForeignKey("chart.song_id"), primary_key=True)
    rating_class: Mapped[str] = mapped_column(
        ForeignKey("chart.rating_class"), primary_key=True
    )
    constant: Mapped[int] = mapped_column(
        comment="real_constant * 10. For example, Crimson Throne [FTR] is 10.4, then store 104 here."
    )
    note: Mapped[Optional[int]]
