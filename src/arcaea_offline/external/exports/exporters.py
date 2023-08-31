from ...models import Score
from .types import ScoreExport


def score(score: Score) -> ScoreExport:
    return {
        "id": score.id,
        "song_id": score.song_id,
        "rating_class": score.rating_class,
        "score": score.score,
        "pure": score.pure,
        "far": score.far,
        "lost": score.lost,
        "date": score.date,
        "max_recall": score.max_recall,
        "modifier": score.modifier,
        "clear_type": score.clear_type,
        "comment": score.comment,
    }
