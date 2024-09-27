import sqlite3

import tests.resources
from arcaea_offline.constants.enums.arcaea import ArcaeaRatingClass
from arcaea_offline.database.models.v5 import ChartInfo
from arcaea_offline.external.importers.chart_info_database import (
    ChartInfoDatabaseParser,
)

db = sqlite3.connect(":memory:")
db.executescript(tests.resources.get_resource("cidb.sql").read_text(encoding="utf-8"))


class TestChartInfoDatabaseParser:
    def test_parse(self):
        items = ChartInfoDatabaseParser.parse(db)
        assert all(isinstance(item, ChartInfo) for item in items)

        assert len(items) == 3

        test1 = next(filter(lambda x: x.song_id == "test1", items))
        assert test1.rating_class is ArcaeaRatingClass.PRESENT
        assert test1.constant == 90
        assert test1.notes == 900

        test2 = next(filter(lambda x: x.song_id == "test2", items))
        assert test2.rating_class is ArcaeaRatingClass.FUTURE
        assert test2.constant == 95
        assert test2.notes == 950

        test3 = next(filter(lambda x: x.song_id == "test3", items))
        assert test3.rating_class is ArcaeaRatingClass.BEYOND
        assert test3.constant == 100
        assert test3.notes is None
