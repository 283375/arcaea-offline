import contextlib
import sqlite3
from typing import List

from sqlalchemy.orm import Session

from ...models.songs import ChartInfo


class ChartInfoDbParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self) -> List[ChartInfo]:
        results = []
        with sqlite3.connect(self.filepath) as conn:
            with contextlib.closing(conn.cursor()) as cursor:
                db_results = cursor.execute(
                    "SELECT song_id, rating_class, constant, notes FROM charts_info"
                ).fetchall()
                for result in db_results:
                    chart = ChartInfo(
                        song_id=result[0],
                        rating_class=result[1],
                        constant=result[2],
                        notes=result[3] or None,
                    )
                    results.append(chart)

        return results

    def write_database(self, session: Session):
        results = self.parse()
        for result in results:
            session.merge(result)
