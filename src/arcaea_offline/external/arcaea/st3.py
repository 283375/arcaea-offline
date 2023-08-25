import sqlite3
from typing import List

from ...models.scores import Score
from .common import ArcaeaParser


class St3ScoreParser(ArcaeaParser):
    CLEAR_TYPES_MAP = {0: -1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1}

    def __init__(self, filepath):
        super().__init__(filepath)

    def parse(self) -> List[Score]:
        items = []
        with sqlite3.connect(self.filepath) as st3_conn:
            cursor = st3_conn.cursor()
            db_scores = cursor.execute(
                "SELECT songId, songDifficulty, score, perfectCount, nearCount, missCount, date FROM scores"
            ).fetchall()
            for song_id, rating_class, score, pure, far, lost, date in db_scores:
                db_clear_type = cursor.execute(
                    "SELECT clearType FROM cleartypes WHERE songId = ? AND songDifficulty = ?",
                    (song_id, rating_class),
                ).fetchone()[0]
                r10_clear_type = self.CLEAR_TYPES_MAP[db_clear_type]

                date_str = str(date)
                date = None if len(date_str) < 7 else int(date_str.ljust(10, "0"))

                items.append(
                    Score(
                        song_id=song_id,
                        rating_class=rating_class,
                        score=score,
                        pure=pure,
                        far=far,
                        lost=lost,
                        date=date,
                        r10_clear_type=r10_clear_type,
                    )
                )

        return items
