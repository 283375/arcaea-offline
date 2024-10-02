import sqlite3

import tests.resources
from arcaea_offline.constants.enums.arcaea import ArcaeaRatingClass
from arcaea_offline.database.models import ChartInfo
from arcaea_offline.external.importers.arcsong import (
    ArcsongDatabaseImporter,
)

db = sqlite3.connect(":memory:")
db.executescript(
    tests.resources.get_resource("arcsong.sql").read_text(encoding="utf-8")
)


class TestArcsongDatabaseImporter:
    def test_parse(self):
        items = ArcsongDatabaseImporter.parse(db)

        assert all(isinstance(item, ChartInfo) for item in items)
        assert len(items) == 3

        base1_pst = next(
            it
            for it in items
            if it.song_id == "base1" and it.rating_class is ArcaeaRatingClass.PAST
        )
        assert base1_pst.constant == 30
        assert base1_pst.notes == 500

        base1_prs = next(
            it
            for it in items
            if it.song_id == "base1" and it.rating_class is ArcaeaRatingClass.PRESENT
        )
        assert base1_prs.constant == 60
        assert base1_prs.notes == 700

        base1_ftr = next(
            it
            for it in items
            if it.song_id == "base1" and it.rating_class is ArcaeaRatingClass.FUTURE
        )
        assert base1_ftr.constant == 90
        assert base1_ftr.notes == 1000
