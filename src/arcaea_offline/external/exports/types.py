from typing import Optional, TypedDict


class ScoreExport(TypedDict):
    id: int
    song_id: str
    rating_class: int
    score: int
    pure: Optional[int]
    far: Optional[int]
    lost: Optional[int]
    date: Optional[int]
    max_recall: Optional[int]
    modifier: Optional[int]
    clear_type: Optional[int]
    comment: Optional[str]
