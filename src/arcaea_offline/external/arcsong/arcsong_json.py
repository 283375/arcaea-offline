import logging
import re
from typing import List, Optional, TypedDict

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ...models import (
    ChartInfo,
    Difficulty,
    DifficultyLocalized,
    Pack,
    Song,
    SongLocalized,
)

logger = logging.getLogger(__name__)


class TArcSongJsonDifficultyItem(TypedDict):
    name_en: str
    name_jp: str
    artist: str
    bpm: str
    bpm_base: float
    set: str
    set_friendly: str
    time: int
    side: int
    world_unlock: bool
    remote_download: bool
    bg: str
    date: int
    version: str
    difficulty: int
    rating: int
    note: int
    chart_designer: str
    jacket_designer: str
    jacket_override: bool
    audio_override: bool


class TArcSongJsonSongItem(TypedDict):
    song_id: str
    difficulties: List[TArcSongJsonDifficultyItem]
    alias: List[str]


class TArcSongJson(TypedDict):
    songs: List[TArcSongJsonSongItem]


class ArcSongJsonBuilder:
    def __init__(self, session: Session):
        self.session = session

    def get_difficulty_item(
        self,
        difficulty: Difficulty,
        song: Song,
        pack: Pack,
        song_localized: Optional[SongLocalized],
    ) -> TArcSongJsonDifficultyItem:
        if "_append_" in pack.id:
            base_pack = self.session.scalar(
                select(Pack).where(Pack.id == re.sub(r"_append_.*$", "", pack.id))
            )
        else:
            base_pack = None

        difficulty_localized = self.session.scalar(
            select(DifficultyLocalized).where(
                (DifficultyLocalized.song_id == difficulty.song_id)
                & (DifficultyLocalized.rating_class == difficulty.rating_class)
            )
        )
        chart_info = self.session.scalar(
            select(ChartInfo).where(
                (ChartInfo.song_id == difficulty.song_id)
                & (ChartInfo.rating_class == difficulty.rating_class)
            )
        )

        if difficulty_localized:
            name_jp = difficulty_localized.title_ja or ""
        elif song_localized:
            name_jp = song_localized.title_ja or ""
        else:
            name_jp = ""

        return {
            "name_en": difficulty.title or song.title,
            "name_jp": name_jp,
            "artist": difficulty.artist or song.artist,
            "bpm": difficulty.bpm or song.bpm or "",
            "bpm_base": difficulty.bpm_base or song.bpm_base or 0.0,
            "set": song.set,
            "set_friendly": f"{base_pack.name} - {pack.name}"
            if base_pack
            else pack.name,
            "time": 0,
            "side": song.side or 0,
            "world_unlock": False,
            "remote_download": False,
            "bg": difficulty.bg or song.bg or "",
            "date": difficulty.date or song.date or 0,
            "version": difficulty.version or song.version or "",
            "difficulty": difficulty.rating * 2 + int(difficulty.rating_plus),
            "rating": chart_info.constant or 0 if chart_info else 0,
            "note": chart_info.notes or 0 if chart_info else 0,
            "chart_designer": difficulty.chart_designer or "",
            "jacket_designer": difficulty.jacket_desginer or "",
            "jacket_override": difficulty.jacket_override,
            "audio_override": difficulty.audio_override,
        }

    def get_song_item(self, song: Song) -> TArcSongJsonSongItem:
        difficulties = self.session.scalars(
            select(Difficulty).where(Difficulty.song_id == song.id)
        )

        pack = self.session.scalar(select(Pack).where(Pack.id == song.set))
        if not pack:
            logger.warning(
                'Cannot find pack "%s", using placeholder instead.', song.set
            )
            pack = Pack(id="unknown", name="Unknown", description="__PLACEHOLDER__")
        song_localized = self.session.scalar(
            select(SongLocalized).where(SongLocalized.id == song.id)
        )

        return {
            "song_id": song.id,
            "difficulties": [
                self.get_difficulty_item(difficulty, song, pack, song_localized)
                for difficulty in difficulties
            ],
            "alias": [],
        }

    def generate_arcsong_json(self) -> TArcSongJson:
        songs = self.session.scalars(select(Song))
        arcsong_songs = []
        for song in songs:
            proceed = self.session.scalar(
                select(func.count(Difficulty.rating_class)).where(
                    Difficulty.song_id == song.id
                )
            )

            if not proceed:
                continue

            arcsong_songs.append(self.get_song_item(song))

        return {"songs": arcsong_songs}
