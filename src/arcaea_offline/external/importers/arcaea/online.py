import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Literal, Optional, TypedDict

from arcaea_offline.constants.enums import (
    ArcaeaPlayResultClearType,
    ArcaeaPlayResultModifier,
    ArcaeaRatingClass,
)
from arcaea_offline.database.models import PlayResult

from .common import fix_timestamp

logger = logging.getLogger(__name__)


class _RatingMePlayResultItem(TypedDict):
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


class _RatingMeValue(TypedDict):
    best_rated_scores: List[_RatingMePlayResultItem]
    recent_rated_scores: List[_RatingMePlayResultItem]


class _RatingMeResponse(TypedDict):
    success: bool
    error_code: Optional[int]
    value: Optional[_RatingMeValue]


class ArcaeaOnlineApiParser:
    def __init__(self, api_result_text: str):
        self.api_result_text = api_result_text
        self.api_result: _RatingMeResponse = json.loads(api_result_text)

    def parse(self) -> List[PlayResult]:
        api_result_value = self.api_result.get("value")
        if not api_result_value:
            error_code = self.api_result.get("error_code")
            raise ValueError(
                f"Cannot parse Arcaea Online API result, error code {error_code}"
            )

        best30_items = api_result_value.get("best_rated_scores", [])
        recent_items = api_result_value.get("recent_rated_scores", [])
        items = best30_items + recent_items

        date_text = (
            datetime.now(tz=timezone.utc).astimezone().isoformat(timespec="seconds")
        )

        results: List[PlayResult] = []
        results_time_played = []
        for item in items:
            date_millis = fix_timestamp(item["time_played"])

            if date_millis in results_time_played:
                # filter out duplicate play results
                continue

            if date_millis:
                date = datetime.fromtimestamp(date_millis / 1000).astimezone()
                results_time_played.append(date_millis)
            else:
                date = None

            play_result = PlayResult()
            play_result.song_id = item["song_id"]
            play_result.rating_class = ArcaeaRatingClass(item["difficulty"])
            play_result.score = item["score"]
            play_result.pure = item["perfect_count"]
            play_result.far = item["near_count"]
            play_result.lost = item["miss_count"]
            play_result.played_at = date
            play_result.modifier = ArcaeaPlayResultModifier(item["modifier"])
            play_result.clear_type = ArcaeaPlayResultClearType(item["clear_type"])

            if play_result.lost == 0:
                play_result.max_recall = play_result.pure + play_result.far

            play_result.comment = f"Parsed from web API at {date_text}"
            results.append(play_result)
        return results
