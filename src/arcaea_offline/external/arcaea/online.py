import json
import logging
from datetime import datetime
from typing import Dict, List, Literal, Optional, TypedDict

from ...models import Score
from .common import ArcaeaParser, fix_timestamp

logger = logging.getLogger(__name__)


class TWebApiRatingMeScoreItem(TypedDict):
    song_id: str
    difficulty: int
    modifier: int
    rating: float
    score: int
    perfect_count: int
    near_count: int
    miss_count: int
    clear_type: int
    title: Dict[Literal["ja", "en"], str]
    artist: str
    time_played: int
    bg: str


class TWebApiRatingMeValue(TypedDict):
    best_rated_scores: List[TWebApiRatingMeScoreItem]
    recent_rated_scores: List[TWebApiRatingMeScoreItem]


class TWebApiRatingMeResult(TypedDict):
    success: bool
    error_code: Optional[int]
    value: Optional[TWebApiRatingMeValue]


class ArcaeaOnlineParser(ArcaeaParser):
    def parse(self) -> List[Score]:
        api_result_root: TWebApiRatingMeResult = json.loads(self.read_file_text())

        api_result_value = api_result_root.get("value")
        if not api_result_value:
            error_code = api_result_root.get("error_code")
            raise ValueError(f"Cannot parse API result, error code {error_code}")

        best30_score_items = api_result_value.get("best_rated_scores", [])
        recent_score_items = api_result_value.get("recent_rated_scores", [])
        score_items = best30_score_items + recent_score_items

        date_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        results: List[Score] = []
        for score_item in score_items:
            score = Score()
            score.song_id = score_item["song_id"]
            score.rating_class = score_item["difficulty"]
            score.score = score_item["score"]
            score.pure = score_item["perfect_count"]
            score.far = score_item["near_count"]
            score.lost = score_item["miss_count"]
            score.date = fix_timestamp(int(score_item["time_played"] / 1000))
            score.modifier = score_item["modifier"]
            score.clear_type = score_item["clear_type"]

            if score.lost == 0:
                score.max_recall = score.pure + score.far

            score.comment = f"Parsed from web API at {date_text}"
            results.append(score)
        return results
