import logging
import sqlite3
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from ...models.scores import Score
from .common import ArcaeaParser, fix_timestamp

logger = logging.getLogger(__name__)


class St3ScoreParser(ArcaeaParser):
    def parse(self) -> List[Score]:
        items = []
        with sqlite3.connect(self.filepath) as st3_conn:
            cursor = st3_conn.cursor()
            db_scores = cursor.execute(
                "SELECT songId, songDifficulty, score, perfectCount, nearCount, missCount, "
                "date, modifier FROM scores"
            ).fetchall()
            for (
                song_id,
                rating_class,
                score,
                pure,
                far,
                lost,
                date,
                modifier,
            ) in db_scores:
                clear_type = cursor.execute(
                    "SELECT clearType FROM cleartypes WHERE songId = ? AND songDifficulty = ?",
                    (song_id, rating_class),
                ).fetchone()[0]

                items.append(
                    Score(
                        song_id=song_id,
                        rating_class=rating_class,
                        score=score,
                        pure=pure,
                        far=far,
                        lost=lost,
                        date=fix_timestamp(date),
                        modifier=modifier,
                        clear_type=clear_type,
                        comment="Parsed from st3",
                    )
                )

        return items

    def write_database(self, session: Session, *, skip_duplicate=True):
        parsed_scores = self.parse()
        for parsed_score in parsed_scores:
            query_score = session.scalar(
                select(Score).where(
                    (Score.song_id == parsed_score.song_id)
                    & (Score.rating_class == parsed_score.rating_class)
                    & (Score.score == parsed_score.score)
                )
            )

            if query_score and skip_duplicate:
                logger.info(
                    "%r skipped because potential duplicate item %r found.",
                    parsed_score,
                    query_score,
                )
                continue
            session.add(parsed_score)
