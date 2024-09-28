from typing import List, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from arcaea_offline.constants.enums.arcaea import ArcaeaRatingClass
from arcaea_offline.database.models.v5 import (
    ChartInfo,
    Difficulty,
    PlayResultBest,
    Song,
)
from arcaea_offline.utils.formatters.rating_class import RatingClassFormatter


class SmartRteBest30CsvExporter:
    CSV_ROWS = [
        "SongName",
        "SongId",
        "Difficulty",
        "Score",
        "Perfect",
        "Perfect+",
        "Far",
        "Lost",
        "Constant",
        "PlayRating",
    ]

    @classmethod
    def rows(cls, session: Session) -> List:
        results: List[
            Tuple[str, str, ArcaeaRatingClass, int, int, int, int, int, float]
        ] = (
            session.query(
                func.coalesce(Difficulty.title, Song.title),
                PlayResultBest.song_id,
                PlayResultBest.rating_class,
                PlayResultBest.score,
                PlayResultBest.pure,
                PlayResultBest.shiny_pure,
                PlayResultBest.far,
                PlayResultBest.lost,
                ChartInfo.constant,
                PlayResultBest.potential,
            )
            .join(
                ChartInfo,
                (ChartInfo.song_id == PlayResultBest.song_id)
                & (ChartInfo.rating_class == PlayResultBest.rating_class),
            )
            .join(Song, (Song.id == PlayResultBest.song_id))
            .join(
                Difficulty,
                (Difficulty.song_id == PlayResultBest.song_id)
                & (Difficulty.rating_class == PlayResultBest.rating_class),
            )
            .all()
        )

        csv_rows = []
        csv_rows.append(cls.CSV_ROWS.copy())
        for _result in results:
            result = list(_result)

            # replace the comma in song title because the target project
            # cannot handle quoted string
            result[0] = result[0].replace(",", "")  # type: ignore
            result[2] = RatingClassFormatter.name(result[2])  # type: ignore
            result[-2] = result[-2] / 10  # type: ignore
            result[-1] = round(result[-1], 5)  # type: ignore

            csv_rows.append(result)

        return csv_rows
