import sqlite3
from typing import List

from sqlalchemy.orm import Session

from ...models.songs import ChartInfo


class ArcsongDbParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self) -> List[ChartInfo]:
        results = []
        with sqlite3.connect(self.filepath) as conn:
            cursor = conn.cursor()
            arcsong_db_results = cursor.execute(
                "SELECT song_id, rating_class, rating, note FROM charts"
            )
            for result in arcsong_db_results:
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
