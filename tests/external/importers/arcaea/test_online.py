import json
from datetime import datetime, timezone

from arcaea_offline.constants.enums.arcaea import (
    ArcaeaPlayResultClearType,
    ArcaeaPlayResultModifier,
    ArcaeaRatingClass,
)
from arcaea_offline.database.models.play_results import PlayResult
from arcaea_offline.external.importers.arcaea.online import ArcaeaOnlineApiParser

API_RESULT = {
    "success": True,
    "value": {
        "best_rated_scores": [
            {
                "song_id": "test1",
                "difficulty": 2,
                "modifier": 0,
                "rating": 12.5,
                "score": 9908123,
                "perfect_count": 1234,
                "near_count": 12,
                "miss_count": 4,
                "clear_type": 1,
                "title": {"ja": "テスト1", "en": "Test 1"},
                "artist": "pytest",
                "time_played": 1704067200000,  # 2024-01-01 00:00:00 UTC
                "bg": "abcdefg123456hijklmn7890123opqrs",
            },
            {
                "song_id": "test2",
                "difficulty": 2,
                "modifier": 0,
                "rating": 12.0,
                "score": 9998123,
                "perfect_count": 1234,
                "near_count": 1,
                "miss_count": 0,
                "clear_type": 1,
                "title": {"ja": "テスト2", "en": "Test 2"},
                "artist": "pytest",
                "time_played": 1704067200000,
                "bg": "abcdefg123456hijklmn7890123opqrs",
            },
        ],
        "recent_rated_scores": [
            {
                "song_id": "test2",
                "difficulty": 2,
                "modifier": 0,
                "rating": 12.0,
                "score": 9998123,
                "perfect_count": 1234,
                "near_count": 1,
                "miss_count": 0,
                "clear_type": 1,
                "title": {"ja": "テスト2", "en": "Test 2"},
                "artist": "pytest",
                "time_played": 1704153600000,  # 2024-01-02 00:00:00 UTC
                "bg": "abcdefg123456hijklmn7890123opqrs",
            }
        ],
    },
}


class TestArcaeaOnlineApiParser:
    API_RESULT_CONTENT = json.dumps(API_RESULT, ensure_ascii=False)

    def test_parse(self):
        play_results = ArcaeaOnlineApiParser(self.API_RESULT_CONTENT).parse()
        assert all(isinstance(item, PlayResult) for item in play_results)

        assert len(play_results) == 2

        test1 = next(filter(lambda x: x.song_id == "test1", play_results))
        assert test1.rating_class is ArcaeaRatingClass.FUTURE
        assert test1.score == 9908123
        assert test1.pure == 1234
        assert test1.far == 12
        assert test1.lost == 4
        assert test1.date == datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert test1.clear_type is ArcaeaPlayResultClearType.NORMAL_CLEAR
        assert test1.modifier is ArcaeaPlayResultModifier.NORMAL

        test2 = next(filter(lambda x: x.song_id == "test2", play_results))
        assert test2.date == datetime(2024, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
