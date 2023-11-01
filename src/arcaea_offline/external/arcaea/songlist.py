import json
from typing import List, Union

from ...models.songs import Difficulty, DifficultyLocalized, Song, SongLocalized
from .common import ArcaeaParser, is_localized, set_model_localized_attrs, to_db_value


class SonglistParser(ArcaeaParser):
    def parse(
        self,
    ) -> List[Union[Song, SongLocalized, Difficulty, DifficultyLocalized]]:
        songlist_json_root = json.loads(self.read_file_text())

        songlist_json = songlist_json_root["songs"]
        results = []
        for item in songlist_json:
            song = Song()
            song.idx = item["idx"]
            song.id = item["id"]
            song.title = item["title_localized"]["en"]
            song.artist = item["artist"]
            song.bpm = item["bpm"]
            song.bpm_base = item["bpm_base"]
            song.set = item["set"]
            song.audio_preview = item["audioPreview"]
            song.audio_preview_end = item["audioPreviewEnd"]
            song.side = item["side"]
            song.version = item["version"]
            song.date = item["date"]
            song.bg = to_db_value(item.get("bg"))
            song.bg_inverse = to_db_value(item.get("bg_inverse"))
            if item.get("bg_daynight"):
                song.bg_day = to_db_value(item["bg_daynight"].get("day"))
                song.bg_night = to_db_value(item["bg_daynight"].get("night"))
            if item.get("source_localized"):
                song.source = item["source_localized"]["en"]
            song.source_copyright = to_db_value(item.get("source_copyright"))
            results.append(song)

            if (
                is_localized(item, "title")
                or is_localized(item, "search_title", append_localized=False)
                or is_localized(item, "search_artist", append_localized=False)
                or is_localized(item, "source")
            ):
                song_localized = SongLocalized(id=song.id)
                set_model_localized_attrs(song_localized, item, "title")
                set_model_localized_attrs(
                    song_localized, item, "search_title", "search_title"
                )
                set_model_localized_attrs(
                    song_localized, item, "search_artist", "search_artist"
                )
                set_model_localized_attrs(song_localized, item, "source")
                results.append(song_localized)

        return results


class SonglistDifficultiesParser(ArcaeaParser):
    def parse(self) -> List[Union[Difficulty, DifficultyLocalized]]:
        songlist_json_root = json.loads(self.read_file_text())

        songlist_json = songlist_json_root["songs"]
        results = []
        for song_item in songlist_json:
            if not song_item.get("difficulties"):
                continue

            for item in song_item["difficulties"]:
                if item["rating"] == 0:
                    continue

                chart = Difficulty(song_id=song_item["id"])
                chart.rating_class = item["ratingClass"]
                chart.rating = item["rating"]
                chart.rating_plus = item.get("ratingPlus") or False
                chart.chart_designer = item["chartDesigner"]
                chart.jacket_desginer = item.get("jacketDesigner") or None
                chart.audio_override = item.get("audioOverride") or False
                chart.jacket_override = item.get("jacketOverride") or False
                chart.jacket_night = item.get("jacketNight") or None
                chart.title = item.get("title_localized", {}).get("en") or None
                chart.artist = item.get("artist") or None
                chart.bg = item.get("bg") or None
                chart.bg_inverse = item.get("bg_inverse")
                chart.bpm = item.get("bpm") or None
                chart.bpm_base = item.get("bpm_base") or None
                chart.version = item.get("version") or None
                chart.date = item.get("date") or None
                results.append(chart)

                if is_localized(item, "title") or is_localized(item, "artist"):
                    chart_localized = DifficultyLocalized(
                        song_id=chart.song_id, rating_class=chart.rating_class
                    )
                    set_model_localized_attrs(chart_localized, item, "title")
                    set_model_localized_attrs(chart_localized, item, "artist")
                    results.append(chart_localized)

        return results
