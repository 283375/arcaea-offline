from typing import List, TypedDict


class ArcsongJsonDifficultyItem(TypedDict):
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


class ArcsongJsonSongItem(TypedDict):
    song_id: str
    difficulties: List[ArcsongJsonDifficultyItem]
    alias: List[str]


class ArcsongJsonRoot(TypedDict):
    songs: List[ArcsongJsonSongItem]
