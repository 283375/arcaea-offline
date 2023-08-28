from decimal import Decimal
from math import floor
from typing import Dict, List

from .models.scores import ScoreCalculated


def calculate_score_range(notes: int, pure: int, far: int):
    single_note_score = 10000000 / Decimal(notes)

    actual_score = floor(
        single_note_score * pure + single_note_score * Decimal(0.5) * far
    )
    return (actual_score, actual_score + pure)


def calculate_potential(_constant: float, score: int) -> Decimal:
    constant = Decimal(_constant)
    if score >= 10000000:
        return constant + 2
    elif score >= 9800000:
        return constant + 1 + (Decimal(score - 9800000) / 200000)
    else:
        return max(Decimal(0), constant + (Decimal(score - 9500000) / 300000))


def calculate_shiny_pure(notes: int, score: int, pure: int, far: int) -> int:
    single_note_score = 10000000 / Decimal(notes)
    actual_score = single_note_score * pure + single_note_score * Decimal(0.5) * far
    return score - floor(actual_score)


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
