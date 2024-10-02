"""
Game database play results importer
"""

import logging
import sqlite3
from datetime import datetime, timezone
from typing import List, overload

from arcaea_offline.constants.enums import (
    ArcaeaPlayResultClearType,
    ArcaeaPlayResultModifier,
    ArcaeaRatingClass,
)
from arcaea_offline.database.models import PlayResult

from .common import fix_timestamp

logger = logging.getLogger(__name__)


class ArcaeaSt3Parser:
    @classmethod
    @overload
    def parse(cls, db: sqlite3.Connection) -> List[PlayResult]: ...

    @classmethod
    @overload
    def parse(cls, db: sqlite3.Cursor) -> List[PlayResult]: ...

    @classmethod
    def parse(cls, db) -> List[PlayResult]:
        if isinstance(db, sqlite3.Connection):
            return cls.parse(db.cursor())

        if not isinstance(db, sqlite3.Cursor):
            raise TypeError(
                "Unknown overload of `db`. Expected `sqlite3.Connection` or `sqlite3.Cursor`."
            )

        entities = []
        query_results = db.execute("""
            SELECT s.id AS _id, s.songId, s.songDifficulty AS ratingClass, s.score,
                s.perfectCount AS pure, s.nearCount AS far, s.missCount AS lost,
                s.`date`, s.modifier, ct.clearType
            FROM scores s JOIN cleartypes ct
            ON s.songId = ct.songId AND s.songDifficulty = ct.songDifficulty""")
        # maybe `s.id = ct.id`?

        now = datetime.now(tz=timezone.utc)
        import_comment = (
            f"Imported from st3 at {now.astimezone().isoformat(timespec='seconds')}"
        )
        for result in query_results:
            (
                _id,
                song_id,
                rating_class,
                score,
                pure,
                far,
                lost,
                date,
                modifier,
                clear_type,
            ) = result

            try:
                rating_class_enum = ArcaeaRatingClass(rating_class)
            except ValueError:
                logger.warning(
                    "Unknown rating class [%r] at entry id %d, skipping!",
                    rating_class,
                    _id,
                )
                continue

            try:
                clear_type_enum = ArcaeaPlayResultClearType(clear_type)
            except ValueError:
                logger.warning(
                    "Unknown clear type [%r] at entry id %d, falling back to `None`!",
                    clear_type,
                    _id,
                )
                clear_type_enum = None

            try:
                modifier_enum = ArcaeaPlayResultModifier(modifier)
            except ValueError:
                logger.warning(
                    "Unknown modifier [%r] at entry id %d, falling back to `None`!",
                    modifier,
                    _id,
                )
                modifier_enum = None

            if date := fix_timestamp(date):
                date = datetime.fromtimestamp(date).astimezone()
            else:
                date = None

            entities.append(
                PlayResult(
                    song_id=song_id,
                    rating_class=rating_class_enum,
                    score=score,
                    pure=pure,
                    far=far,
                    lost=lost,
                    date=date,
                    modifier=modifier_enum,
                    clear_type=clear_type_enum,
                    comment=import_comment,
                )
            )

        return entities
