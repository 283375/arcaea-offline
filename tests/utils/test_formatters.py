import pytest

from arcaea_offline.constants.enums import (
    ArcaeaPlayResultClearType,
    ArcaeaPlayResultModifier,
    ArcaeaRatingClass,
)
from arcaea_offline.utils.formatters.play_result import PlayResultFormatter
from arcaea_offline.utils.formatters.rating_class import RatingClassFormatter


class TestRatingClassFormatter:
    def test_name(self):
        assert RatingClassFormatter.name(ArcaeaRatingClass.PAST) == "Past"
        assert RatingClassFormatter.name(ArcaeaRatingClass.PRESENT) == "Present"
        assert RatingClassFormatter.name(ArcaeaRatingClass.FUTURE) == "Future"
        assert RatingClassFormatter.name(ArcaeaRatingClass.BEYOND) == "Beyond"
        assert RatingClassFormatter.name(ArcaeaRatingClass.ETERNAL) == "Eternal"

        assert RatingClassFormatter.name(2) == "Future"

        assert RatingClassFormatter.name(100) == "Unknown"
        assert RatingClassFormatter.name(-1) == "Unknown"

        pytest.raises(TypeError, RatingClassFormatter.name, "2")
        pytest.raises(TypeError, RatingClassFormatter.name, [])
        pytest.raises(TypeError, RatingClassFormatter.name, None)

    def test_abbreviation(self):
        assert RatingClassFormatter.abbreviation(ArcaeaRatingClass.PAST) == "PST"
        assert RatingClassFormatter.abbreviation(ArcaeaRatingClass.PRESENT) == "PRS"
        assert RatingClassFormatter.abbreviation(ArcaeaRatingClass.FUTURE) == "FTR"
        assert RatingClassFormatter.abbreviation(ArcaeaRatingClass.BEYOND) == "BYD"
        assert RatingClassFormatter.abbreviation(ArcaeaRatingClass.ETERNAL) == "ETR"

        assert RatingClassFormatter.abbreviation(2) == "FTR"

        assert RatingClassFormatter.abbreviation(100) == "UNK"
        assert RatingClassFormatter.abbreviation(-1) == "UNK"

        pytest.raises(TypeError, RatingClassFormatter.abbreviation, "2")
        pytest.raises(TypeError, RatingClassFormatter.abbreviation, [])
        pytest.raises(TypeError, RatingClassFormatter.abbreviation, None)


class TestPlayResultFormatter:
    def test_score_grade(self):
        assert PlayResultFormatter.score_grade(10001284) == "EX+"
        assert PlayResultFormatter.score_grade(9989210) == "EX+"
        assert PlayResultFormatter.score_grade(9900000) == "EX+"

        assert PlayResultFormatter.score_grade(9899999) == "EX"
        assert PlayResultFormatter.score_grade(9843717) == "EX"
        assert PlayResultFormatter.score_grade(9800000) == "EX"

        assert PlayResultFormatter.score_grade(9799999) == "AA"
        assert PlayResultFormatter.score_grade(9794015) == "AA"
        assert PlayResultFormatter.score_grade(9750000) == "AA"

        assert PlayResultFormatter.score_grade(9499999) == "A"
        assert PlayResultFormatter.score_grade(9356855) == "A"
        assert PlayResultFormatter.score_grade(9200000) == "A"

        assert PlayResultFormatter.score_grade(9199999) == "B"
        assert PlayResultFormatter.score_grade(9065785) == "B"
        assert PlayResultFormatter.score_grade(8900000) == "B"

        assert PlayResultFormatter.score_grade(8899999) == "C"
        assert PlayResultFormatter.score_grade(8756211) == "C"
        assert PlayResultFormatter.score_grade(8600000) == "C"

        assert PlayResultFormatter.score_grade(8599999) == "D"
        assert PlayResultFormatter.score_grade(5500000) == "D"
        assert PlayResultFormatter.score_grade(0) == "D"

        pytest.raises(ValueError, PlayResultFormatter.score_grade, -1)
        pytest.raises(TypeError, PlayResultFormatter.score_grade, "10001284")
        pytest.raises(TypeError, PlayResultFormatter.score_grade, [])
        pytest.raises(TypeError, PlayResultFormatter.score_grade, None)

    def test_clear_type(self):
        assert (
            PlayResultFormatter.clear_type(ArcaeaPlayResultClearType.TRACK_LOST)
            == "TRACK LOST"
        )
        assert (
            PlayResultFormatter.clear_type(ArcaeaPlayResultClearType.NORMAL_CLEAR)
            == "NORMAL CLEAR"
        )
        assert (
            PlayResultFormatter.clear_type(ArcaeaPlayResultClearType.FULL_RECALL)
            == "FULL RECALL"
        )
        assert (
            PlayResultFormatter.clear_type(ArcaeaPlayResultClearType.PURE_MEMORY)
            == "PURE MEMORY"
        )
        assert (
            PlayResultFormatter.clear_type(ArcaeaPlayResultClearType.EASY_CLEAR)
            == "EASY CLEAR"
        )
        assert (
            PlayResultFormatter.clear_type(ArcaeaPlayResultClearType.HARD_CLEAR)
            == "HARD CLEAR"
        )
        assert PlayResultFormatter.clear_type(None) == "None"

        assert PlayResultFormatter.clear_type(1) == "NORMAL CLEAR"
        assert PlayResultFormatter.clear_type(6) == "UNKNOWN"

        pytest.raises(ValueError, PlayResultFormatter.clear_type, -1)
        pytest.raises(TypeError, PlayResultFormatter.clear_type, "1")
        pytest.raises(TypeError, PlayResultFormatter.clear_type, [])

    def test_modifier(self):
        assert PlayResultFormatter.modifier(ArcaeaPlayResultModifier.NORMAL) == "NORMAL"
        assert PlayResultFormatter.modifier(ArcaeaPlayResultModifier.EASY) == "EASY"
        assert PlayResultFormatter.modifier(ArcaeaPlayResultModifier.HARD) == "HARD"
        assert PlayResultFormatter.modifier(None) == "None"

        assert PlayResultFormatter.modifier(1) == "EASY"
        assert PlayResultFormatter.modifier(6) == "UNKNOWN"

        pytest.raises(ValueError, PlayResultFormatter.modifier, -1)
        pytest.raises(TypeError, PlayResultFormatter.modifier, "1")
        pytest.raises(TypeError, PlayResultFormatter.modifier, [])
