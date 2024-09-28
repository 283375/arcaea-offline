from typing import List, Literal, Optional, TypedDict


class ArcaeaOfflineDEFv2PlayResultItem(TypedDict, total=False):
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


ArcaeaOfflineDEFv2PlayResultRoot = TypedDict(
    "ArcaeaOfflineDEFv2PlayResultRoot",
    {
        "$schema": Literal[
            "https://arcaeaoffline.sevive.xyz/schemas/def/v2/score.schema.json"
        ],
        "type": Literal["score"],
        "version": Literal[2],
        "scores": List[ArcaeaOfflineDEFv2PlayResultItem],
    },
)
