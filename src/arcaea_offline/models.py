from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class DbChartRow:
    song_id: str
    rating_class: int
    name_en: str
    name_jp: Optional[str]
    artist: str
    bpm: str
    bpm_base: float
    package_id: str
    time: Optional[int]
    side: int
    world_unlock: bool
    remote_download: Optional[bool]
    bg: str
    date: int
    version: str
    difficulty: int
    rating: int
    note: int
    chart_designer: Optional[str]
    jacket_designer: Optional[str]
    jacket_override: bool
    audio_override: bool


@dataclass(kw_only=True)
class Chart:
    song_id: str
    rating_class: int
    name_en: str
    name_jp: Optional[str]
    artist: str
    bpm: str
    bpm_base: float
    package_id: str
    time: Optional[int]
    side: int
    world_unlock: bool
    remote_download: Optional[bool]
    bg: str
    date: int
    version: str
    difficulty: int
    rating: int
    note: int
    chart_designer: Optional[str]
    jacket_designer: Optional[str]
    jacket_override: bool
    audio_override: bool

    @classmethod
    def from_db_row(cls, row: DbChartRow):
        return cls(**asdict(row))


@dataclass
class DbAliasRow:
    song_id: str
    alias: str


@dataclass(kw_only=True)
class Alias:
    song_id: str
    alias: str

    @classmethod
    def from_db_row(cls, row: DbAliasRow):
        return cls(song_id=row.song_id, alias=row.alias)


@dataclass
class DbPackageRow:
    package_id: str
    name: str


@dataclass(kw_only=True)
class Package:
    id: str
    name: str

    @classmethod
    def from_db_row(cls, row: DbPackageRow):
        return cls(id=row.package_id, name=row.name)


@dataclass
class DbScoreRow:
    song_id: str
    rating_class: int
    score: int
    pure: int
    far: int
    lost: int
    time: int
    max_recall: Optional[int] = None


@dataclass(kw_only=True)
class Score:
    song_id: str
    rating_class: int
    score: int
    pure: int
    far: int
    lost: int
    time: int
    max_recall: Optional[int] = None

    @classmethod
    def from_db_row(cls, row: DbScoreRow):
        return cls(**asdict(row))

    def to_db_row(self):
        keys = list(self.__dataclass_fields__)
        values = [self.__getattribute__(key) for key in keys]
        return DbScoreRow(*values)


@dataclass
class DbCalculatedRow:
    song_id: str
    rating_class: int
    score: int
    pure: int
    far: int
    lost: int
    time: int
    rating: int
    note: int
    pure_small: int
    potential: float


@dataclass(kw_only=True)
class Calculated:
    song_id: str
    rating_class: int
    score: int
    pure: int
    far: int
    lost: int
    time: int
    rating: int
    note: int
    pure_small: int
    potential: float

    @classmethod
    def from_db_row(cls, row: DbCalculatedRow):
        return cls(**asdict(row))
