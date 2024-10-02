import sqlite3
from typing import List, overload

from arcaea_offline.constants.enums.arcaea import ArcaeaRatingClass
from arcaea_offline.database.models import ChartInfo


class ArcsongDatabaseImporter:
    @classmethod
    @overload
    def parse(cls, conn: sqlite3.Connection) -> List[ChartInfo]: ...

    @classmethod
    @overload
    def parse(cls, conn: sqlite3.Cursor) -> List[ChartInfo]: ...

    @classmethod
    def parse(cls, conn) -> List[ChartInfo]:
        if isinstance(conn, sqlite3.Connection):
            return cls.parse(conn.cursor())

        assert isinstance(conn, sqlite3.Cursor)

        results = []
        db_results = conn.execute(
            "SELECT song_id, rating_class, rating, note FROM charts"
        )
        for result in db_results:
            results.append(
                ChartInfo(
                    song_id=result[0],
                    rating_class=ArcaeaRatingClass(result[1]),
                    constant=result[2],
                    notes=result[3] or None,
                )
            )

        return results
