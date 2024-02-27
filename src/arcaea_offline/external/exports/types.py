from typing import List, Literal, Optional, TypedDict


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


class ArcaeaOfflineDEFV2_ScoreItem(TypedDict, total=False):
    id: Optional[int]
    songId: str
    ratingClass: int
    score: int
    pure: Optional[int]
    far: Optional[int]
    lost: Optional[int]
    date: Optional[int]
    maxRecall: Optional[int]
    modifier: Optional[int]
    clearType: Optional[int]
    source: Optional[str]
    comment: Optional[str]


ArcaeaOfflineDEFV2_Score = TypedDict(
    "ArcaeaOfflineDEFV2_Score",
    {
        "$schema": Literal[
            "https://arcaeaoffline.sevive.xyz/schemas/def/v2/score.schema.json"
        ],
        "type": Literal["score"],
        "version": Literal[2],
        "scores": List[ArcaeaOfflineDEFV2_ScoreItem],
    },
)
