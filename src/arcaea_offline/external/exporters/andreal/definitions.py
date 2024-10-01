from typing import List, Optional, TypedDict


class AndrealImageGeneratorApiDataAccountInfo(TypedDict):
    name: str
    code: int
    rating: int
    character: int
    is_char_uncapped: bool


class AndrealImageGeneratorApiDataScoreItem(TypedDict):
    score: int
    health: int
    rating: float
    song_id: str
    modifier: int
    difficulty: int
    clear_type: int
    best_clear_type: int
    time_played: int
    near_count: Optional[int]
    miss_count: Optional[int]
    perfect_count: Optional[int]
    shiny_perfect_count: Optional[int]


class AndrealImageGeneratorApiDataContent(TypedDict, total=False):
    account_info: AndrealImageGeneratorApiDataAccountInfo
    recent_score: List[AndrealImageGeneratorApiDataScoreItem]
    record: AndrealImageGeneratorApiDataScoreItem
    best30_avg: float
    best30_list: List[AndrealImageGeneratorApiDataScoreItem]
    best30_overflow: List[AndrealImageGeneratorApiDataScoreItem]


class AndrealImageGeneratorApiDataRoot(TypedDict):
    content: AndrealImageGeneratorApiDataContent
