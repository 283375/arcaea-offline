import logging
import re
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from arcaea_offline.constants.enums.arcaea import ArcaeaLanguage
from arcaea_offline.database.models import Difficulty, Pack, Song

from .definitions import ArcsongJsonDifficultyItem, ArcsongJsonRoot, ArcsongJsonSongItem

logger = logging.getLogger(__name__)


class ArcsongJsonExporter:
    @staticmethod
    def craft_difficulty_item(
        difficulty: Difficulty, *, base_pack: Optional[Pack]
    ) -> ArcsongJsonDifficultyItem:
        song = difficulty.song
        pack = song.pack
        chart_info = difficulty.chart_info

        song_localized_ja = next(
            (lo for lo in song.localized_objects if lo.lang == ArcaeaLanguage.JA),
            None,
        )
        difficulty_localized_ja = next(
            (lo for lo in difficulty.localized_objects if lo.lang == ArcaeaLanguage.JA),
            None,
        )

        if difficulty_localized_ja:
            name_jp = difficulty_localized_ja.title or ""
        elif song_localized_ja:
            name_jp = song_localized_ja.title or ""
        else:
            name_jp = ""

        if difficulty.date is not None:
            date = int(difficulty.date.timestamp())
        elif song.date is not None:
            date = int(song.date.timestamp())
        else:
            date = 0

        return {
            "name_en": difficulty.title or song.title,
            "name_jp": name_jp,
            "artist": difficulty.artist or song.artist,
            "bpm": difficulty.bpm or song.bpm or "",
            "bpm_base": difficulty.bpm_base or song.bpm_base or 0.0,
            "set": song.pack_id,
            "set_friendly": f"{base_pack.name} - {pack.name}"
            if base_pack
            else pack.name,
            "time": 0,
            "side": song.side or 0,
            "world_unlock": False,
            "remote_download": False,
            "bg": difficulty.bg or song.bg or "",
            "date": date,
            "version": difficulty.version or song.version or "",
            "difficulty": difficulty.rating * 2 + int(difficulty.rating_plus),
            "rating": chart_info.constant or 0 if chart_info else 0,
            "note": chart_info.notes or 0 if chart_info else 0,
            "chart_designer": difficulty.chart_designer or "",
            "jacket_designer": difficulty.jacket_desginer or "",
            "jacket_override": difficulty.jacket_override,
            "audio_override": difficulty.audio_override,
        }

    @classmethod
    def craft(cls, session: Session) -> ArcsongJsonRoot:
        songs = session.scalars(select(Song))

        arcsong_songs: List[ArcsongJsonSongItem] = []
        for song in songs:
            if len(song.difficulties) == 0:
                continue

            pack = song.pack
            if "_append_" in pack.id:
                base_pack = session.scalar(
                    select(Pack).where(Pack.id == re.sub(r"_append_.*$", "", pack.id))
                )
            else:
                base_pack = None

            arcsong_difficulties = []
            for difficulty in song.difficulties:
                arcsong_difficulties.append(
                    cls.craft_difficulty_item(difficulty, base_pack=base_pack)
                )

            arcsong_songs.append(
                {
                    "song_id": song.id,
                    "difficulties": arcsong_difficulties,
                    "alias": [],
                }
            )

        return {"songs": arcsong_songs}
