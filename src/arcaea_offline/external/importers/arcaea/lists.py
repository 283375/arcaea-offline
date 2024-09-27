"""
packlist and songlist parsers
"""

import json
from typing import List, Union

from arcaea_offline.constants.enums import (
    ArcaeaLanguage,
    ArcaeaRatingClass,
    ArcaeaSongSide,
)
from arcaea_offline.database.models.v5 import (
    Difficulty,
    DifficultyLocalized,
    Pack,
    PackLocalized,
    Song,
    SongLocalized,
    SongSearchWord,
)


class ArcaeaListParser:
    def __init__(self, list_text: str):
        self.list_text = list_text


class ArcaeaPacklistParser(ArcaeaListParser):
    def parse(self) -> List[Union[Pack, PackLocalized]]:
        root = json.loads(self.list_text)

        packs = root["packs"]
        results: List[Union[Pack, PackLocalized]] = [
            Pack(id="single", name="Memory Archive")
        ]
        for item in packs:
            pack = Pack()
            pack.id = item["id"]
            pack.name = item["name_localized"]["en"]
            pack.description = item["description_localized"]["en"] or None
            results.append(pack)

            for key in ArcaeaLanguage:
                name_localized = item["name_localized"].get(key.value, None)
                description_localized = item["description_localized"].get(
                    key.value, None
                )

                if name_localized or description_localized:
                    pack_localized = PackLocalized(id=pack.id)
                    pack_localized.lang = key.value
                    pack_localized.name = name_localized
                    pack_localized.description = description_localized
                    results.append(pack_localized)

        return results


class ArcaeaSonglistParser(ArcaeaListParser):
    def parse_songs(self) -> List[Union[Song, SongLocalized, SongSearchWord]]:
        root = json.loads(self.list_text)

        songs = root["songs"]
        results = []
        for item in songs:
            song = Song()
            song.idx = item["idx"]
            song.id = item["id"]
            song.title = item["title_localized"]["en"]
            song.artist = item["artist"]
            song.bpm = item["bpm"]
            song.bpm_base = item["bpm_base"]
            song.pack_id = item["set"]
            song.audio_preview = item["audioPreview"]
            song.audio_preview_end = item["audioPreviewEnd"]
            song.side = ArcaeaSongSide(item["side"])
            song.version = item["version"]
            song.date = item["date"]
            song.bg = item.get("bg")
            song.bg_inverse = item.get("bg_inverse")
            if item.get("bg_daynight"):
                song.bg_day = item["bg_daynight"].get("day")
                song.bg_night = item["bg_daynight"].get("night")
            if item.get("source_localized"):
                song.source = item["source_localized"]["en"]
            song.source_copyright = item.get("source_copyright")
            results.append(song)

            for lang in ArcaeaLanguage:
                # SongLocalized objects
                title_localized = item["title_localized"].get(lang.value, None)
                source_localized = item.get("source_localized", {}).get(
                    lang.value, None
                )

                if title_localized or source_localized:
                    song_localized = SongLocalized(id=song.id)
                    song_localized.lang = lang.value
                    song_localized.title = title_localized
                    song_localized.source = source_localized
                    results.append(song_localized)

                # SongSearchTitle
                search_titles = item.get("search_title", {}).get(lang.value, None)
                if search_titles:
                    for search_title in search_titles:
                        song_search_word = SongSearchWord(
                            id=song.id, lang=lang.value, type=1, value=search_title
                        )
                        results.append(song_search_word)

                search_artists = item.get("search_artist", {}).get(lang.value, None)
                if search_artists:
                    for search_artist in search_artists:
                        song_search_word = SongSearchWord(
                            id=song.id, lang=lang.value, type=2, value=search_artist
                        )
                        results.append(song_search_word)

        return results

    def parse_difficulties(self) -> List[Union[Difficulty, DifficultyLocalized]]:
        root = json.loads(self.list_text)

        songs = root["songs"]
        results = []
        for song in songs:
            difficulties = song.get("difficulties")
            if not difficulties:
                continue

            for item in difficulties:
                if item["rating"] == 0:
                    continue

                difficulty = Difficulty()
                difficulty.song_id = song["id"]
                difficulty.rating_class = ArcaeaRatingClass(item["ratingClass"])
                difficulty.rating = item["rating"]
                difficulty.rating_plus = item.get("ratingPlus") or False
                difficulty.chart_designer = item["chartDesigner"]
                difficulty.jacket_desginer = item.get("jacketDesigner") or None
                difficulty.audio_override = item.get("audioOverride") or False
                difficulty.jacket_override = item.get("jacketOverride") or False
                difficulty.jacket_night = item.get("jacketNight") or None
                difficulty.title = item.get("title_localized", {}).get("en") or None
                difficulty.artist = item.get("artist") or None
                difficulty.bg = item.get("bg") or None
                difficulty.bg_inverse = item.get("bg_inverse")
                difficulty.bpm = item.get("bpm") or None
                difficulty.bpm_base = item.get("bpm_base") or None
                difficulty.version = item.get("version") or None
                difficulty.date = item.get("date") or None
                results.append(difficulty)

                for lang in ArcaeaLanguage:
                    title_localized = item.get("title_localized", {}).get(
                        lang.value, None
                    )
                    artist_localized = item.get("artist_localized", {}).get(
                        lang.value, None
                    )

                    if title_localized or artist_localized:
                        difficulty_localized = DifficultyLocalized(
                            song_id=difficulty.song_id,
                            rating_class=difficulty.rating_class,
                        )
                        difficulty_localized.lang = lang.value
                        difficulty_localized.title = title_localized
                        difficulty_localized.artist = artist_localized
                        results.append(difficulty_localized)

        return results

    def parse_all(self):
        return self.parse_songs() + self.parse_difficulties()
