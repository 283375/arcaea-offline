from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Mapped
from sqlalchemy_utils import create_view

from ._base import ModelBase, ModelViewBase, ReprHelper
from .chart_info import ChartInfo
from .difficulty import Difficulty
from .song import Song


class Chart(ModelBase, ReprHelper):
    __tablename__ = "charts"

    song_idx: Mapped[int]
    song_id: Mapped[str]
    rating_class: Mapped[int]
    rating: Mapped[int]
    is_rating_plus: Mapped[bool]
    title: Mapped[str]
    artist: Mapped[str]
    pack_id: Mapped[str]
    bpm: Mapped[Optional[str]]
    bpm_base: Mapped[Optional[float]]
    audio_preview: Mapped[Optional[int]]
    audio_preview_end: Mapped[Optional[int]]
    side: Mapped[Optional[int]]
    version: Mapped[Optional[str]]
    added_at: Mapped[Optional[datetime]]
    bg: Mapped[Optional[str]]
    bg_inverse: Mapped[Optional[str]]
    bg_day: Mapped[Optional[str]]
    bg_night: Mapped[Optional[str]]
    source: Mapped[Optional[str]]
    source_copyright: Mapped[Optional[str]]
    chart_designer: Mapped[Optional[str]]
    jacket_desginer: Mapped[Optional[str]]
    has_overriding_audio: Mapped[bool]
    has_overriding_jacket: Mapped[bool]
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
            Difficulty.is_rating_plus,
            func.coalesce(Difficulty.title, Song.title).label("title"),
            func.coalesce(Difficulty.artist, Song.artist).label("artist"),
            Song.pack_id,
            func.coalesce(Difficulty.bpm, Song.bpm).label("bpm"),
            func.coalesce(Difficulty.bpm_base, Song.bpm_base).label("bpm_base"),
            Song.side,
            func.coalesce(Difficulty.version, Song.version).label("version"),
            func.coalesce(Difficulty.added_at, Song.added_at).label("added_at"),
            func.coalesce(Difficulty.bg, Song.bg).label("bg"),
            func.coalesce(Difficulty.bg_inverse, Song.bg_inverse).label("bg_inverse"),
            Song.bg_day,
            Song.bg_night,
            Song.source,
            Song.source_copyright,
            Difficulty.chart_designer,
            Difficulty.jacket_designer,
            Difficulty.has_overriding_audio,
            Difficulty.has_overriding_jacket,
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
        metadata=ModelViewBase.metadata,
        cascade_on_drop=False,
    )
