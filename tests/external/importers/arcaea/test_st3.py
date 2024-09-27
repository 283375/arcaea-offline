import sqlite3
from datetime import datetime

import pytest

import tests.resources
from arcaea_offline.constants.enums.arcaea import (
    ArcaeaPlayResultClearType,
    ArcaeaPlayResultModifier,
    ArcaeaRatingClass,
)
from arcaea_offline.external.importers.arcaea.st3 import ArcaeaSt3Parser

db = sqlite3.connect(":memory:")
db.executescript(tests.resources.get_resource("st3.sql").read_text(encoding="utf-8"))


class TestArcaeaSt3Parser:
    @property
    def play_results(self):
        return ArcaeaSt3Parser.parse(db)

    def test_basic(self):
        play_results = self.play_results

        assert len(play_results) == 4

        test1 = next(filter(lambda x: x.song_id == "test1", play_results))
        assert test1.rating_class is ArcaeaRatingClass.FUTURE
        assert test1.score == 9441167
        assert test1.pure == 895
        assert test1.far == 32
        assert test1.lost == 22
        assert test1.date == datetime.fromtimestamp(1722100000).astimezone()
        assert test1.clear_type is ArcaeaPlayResultClearType.TRACK_LOST
        assert test1.modifier is ArcaeaPlayResultModifier.HARD

    def test_corrupt_handling(self):
        play_results = self.play_results

        corrupt1 = filter(lambda x: x.song_id == "corrupt1", play_results)
        # `rating_class` out of range, so this should be ignored during parsing,
        # thus does not present in the result.
        assert len(list(corrupt1)) == 0

        corrupt2 = next(filter(lambda x: x.song_id == "corrupt2", play_results))
        assert corrupt2.clear_type is None
        assert corrupt2.modifier is None

        date1 = next(filter(lambda x: x.song_id == "date1", play_results))
        assert date1.date is None

    def test_invalid_input(self):
        pytest.raises(TypeError, ArcaeaSt3Parser.parse, "abcdefghijklmn")
        pytest.raises(TypeError, ArcaeaSt3Parser.parse, 123456)
