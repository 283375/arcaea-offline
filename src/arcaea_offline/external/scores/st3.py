import sqlite3
from typing import Union

from .common import ExternalScoreItem, ExternalScoreSource


class St3ScoreSource(ExternalScoreSource):
    db_path: Union[str, bytes]
    CLEAR_TYPES_MAP = {0: -1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1}

    def __init__(self, db_path: Union[str, bytes]):
        self.db_path = db_path

    def get_score_items(self):
        items = []
        with sqlite3.connect(self.db_path) as st3_conn:
            cursor = st3_conn.cursor()
            db_scores = cursor.execute(
                "SELECT songId, songDifficulty, score, perfectCount, nearCount, missCount, date FROM scores"
            ).fetchall()
            for song_id, rating_class, score, pure, far, lost, date in db_scores:
                db_clear_type = cursor.execute(
                    "SELECT clearType FROM cleartypes WHERE songId = ? AND songDifficulty = ?",
                    (song_id, rating_class),
                ).fetchone()[0]
                clear_type = self.CLEAR_TYPES_MAP[db_clear_type]

                date_str = str(date)
                date = None if len(date_str) < 7 else int(date_str.ljust(10, "0"))

                kwargs = {
                    "song_id": song_id,
                    "rating_class": rating_class,
                    "score": score,
                    "pure": pure,
                    "far": far,
                    "lost": lost,
                    "clear_type": clear_type,
                }
                if date:
                    kwargs["time"] = date
                items.append(ExternalScoreItem(**kwargs))
        return items
