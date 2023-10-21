from sqlalchemy.orm import Session

from ...models import Chart, ScoreBest
from ...utils.rating import rating_class_to_text


class SmartRteB30CsvConverter:
    CSV_ROWS = [
        "songname",
        "songId",
        "Difficulty",
        "score",
        "Perfect",
        "criticalPerfect",
        "Far",
        "Lost",
        "Constant",
        "singlePTT",
    ]

    def __init__(
        self,
        session: Session,
    ):
        self.session = session

    def rows(self) -> list:
        csv_rows = [self.CSV_ROWS.copy()]

        with self.session as session:
            results = (
                session.query(
                    Chart.title,
                    ScoreBest.song_id,
                    ScoreBest.rating_class,
                    ScoreBest.score,
                    ScoreBest.pure,
                    ScoreBest.shiny_pure,
                    ScoreBest.far,
                    ScoreBest.lost,
                    Chart.constant,
                    ScoreBest.potential,
                )
                .join(
                    Chart,
                    (Chart.song_id == ScoreBest.song_id)
                    & (Chart.rating_class == ScoreBest.rating_class),
                )
                .all()
            )

            for result in results:
                # replace the comma in song title because the target project
                # cannot handle quoted string
                result = list(result)
                result[0] = result[0].replace(",", "")
                result[2] = rating_class_to_text(result[2])
                # divide constant to float
                result[-2] = result[-2] / 10
                # round potential
                result[-1] = round(result[-1], 5)
                csv_rows.append(result)

        return csv_rows
