from decimal import Decimal
from typing import Dict, List

from ..models.scores import ScoreCalculated


def get_b30_calculated_list(
    calculated_list: List[ScoreCalculated],
) -> List[ScoreCalculated]:
    best_scores: Dict[str, ScoreCalculated] = {}
    for calculated in calculated_list:
        key = f"{calculated.song_id}_{calculated.rating_class}"
        stored = best_scores.get(key)
        if stored and stored.score < calculated.score or not stored:
            best_scores[key] = calculated
    ret_list = list(best_scores.values())
    ret_list = sorted(ret_list, key=lambda c: c.potential, reverse=True)[:30]
    return ret_list


def calculate_b30(calculated_list: List[ScoreCalculated]) -> Decimal:
    ptt_list = [Decimal(c.potential) for c in get_b30_calculated_list(calculated_list)]
    sum_ptt_list = sum(ptt_list)
    return (sum_ptt_list / len(ptt_list)) if sum_ptt_list else Decimal("0.0")
