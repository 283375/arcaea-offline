import dataclasses
from typing import List


@dataclasses.dataclass
class ExternalScoreItem:
    song_id: str
    rating_class: int
    score: int
    pure: int = -1
    far: int = -1
    lost: int = -1
    max_recall: int = -1
    clear_type: int = -1
    time: int = -1


class ExternalScoreSource:
    def get_score_items(self) -> List[ExternalScoreItem]:
        ...
