import sqlite3
from contextlib import closing
from typing import List, overload

from arcaea_offline.constants.enums.arcaea import ArcaeaRatingClass
from arcaea_offline.database.models import ChartInfo


class ChartInfoDatabaseParser:
    @classmethod
    @overload
    def parse(cls, conn: sqlite3.Connection) -> List[ChartInfo]: ...

    @classmethod
    @overload
    def parse(cls, conn: sqlite3.Cursor) -> List[ChartInfo]: ...

    @classmethod
    def parse(cls, conn) -> List[ChartInfo]:
        if isinstance(conn, sqlite3.Connection):
            with closing(conn.cursor()) as cur:
                return cls.parse(cur)

        if not isinstance(conn, sqlite3.Cursor):
            raise ValueError("conn must be sqlite3.Connection or sqlite3.Cursor!")

        db_items = conn.execute(
            "SELECT song_id, rating_class, constant, notes FROM charts_info"
        ).fetchall()

        results: List[ChartInfo] = []
        for item in db_items:
            (song_id, rating_class, constant, notes) = item

            chart_info = ChartInfo()
            chart_info.song_id = song_id
            chart_info.rating_class = ArcaeaRatingClass(rating_class)
            chart_info.constant = constant
            chart_info.notes = notes

            results.append(chart_info)
        return results
