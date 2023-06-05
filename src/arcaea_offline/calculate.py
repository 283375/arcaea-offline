from decimal import Decimal
from math import floor
from typing import Dict, List

from .models import Calculated, Chart, Score


def calculate_score(chart: Chart, score: Score) -> Calculated:
    assert chart.song_id == score.song_id
    assert chart.rating_class == score.rating_class

    single_note_score = 10000000 / Decimal(chart.note)
    actual_score = (
        single_note_score * score.pure + single_note_score * Decimal(0.5) * score.far
    )
    pure_small = score.score - floor(actual_score)

    constant = Decimal(chart.rating) / 10
    if score.score >= 10000000:
        potential = constant + 2
    elif score.score >= 9800000:
        potential = constant + 1 + (Decimal(score.score - 9800000) / 200000)
    else:
        potential = max(
            Decimal(0), constant + (Decimal(score.score - 9500000) / 300000)
        )
    assert isinstance(potential, Decimal)

    return Calculated(
        song_id=chart.song_id,
        rating_class=chart.rating_class,
        score=score.score,
        pure=score.pure,
        far=score.far,
        lost=score.lost,
        time=score.time,
        rating=chart.rating,
        note=chart.note,
        pure_small=pure_small,
        potential=float(potential),
    )


def get_b30_calculated_list(calculated_list: List[Calculated]) -> List[Calculated]:
    best_scores: Dict[str, Calculated] = {}
    for calculated in calculated_list:
        key = f"{calculated.song_id}_{calculated.rating_class}"
        stored = best_scores.get(key)
        if stored and stored.score < calculated.score or not stored:
            best_scores[key] = calculated
    ret_list = list(best_scores.values())
    ret_list = sorted(ret_list, key=lambda c: c.potential, reverse=True)[:30]
    return ret_list


def calculate_b30(calculated_list: List[Calculated]) -> Decimal:
    ptt_list = [Decimal(c.potential) for c in get_b30_calculated_list(calculated_list)]
    sum_ptt_list = sum(ptt_list)
    return (sum_ptt_list / len(ptt_list)) if sum_ptt_list else Decimal("0.0")


def get_r10_calculated_list(calculated_list: List[Calculated]) -> List[Calculated]:
    recent_scores: Dict[str, Calculated] = {}
    for calculated in calculated_list:
        key = f"{calculated.song_id}_{calculated.rating_class}"
        stored = recent_scores.get(key)
        if stored is None or stored.time < calculated.time:
            recent_scores[key] = calculated
    ret_list = list(recent_scores.values())
    ret_list = sorted(ret_list, key=lambda c: c.time, reverse=True)[:10]
    return ret_list


def calculate_r10(calculated_list: List[Calculated]) -> Decimal:
    ptt_list = [Decimal(c.potential) for c in get_r10_calculated_list(calculated_list)]
    sum_ptt_list = sum(ptt_list)
    return (sum_ptt_list / len(ptt_list)) if sum_ptt_list else Decimal("0.0")


def calculate_potential(calculated_list: List[Calculated]) -> Decimal:
    b30_ptt_list = [
        Decimal(c.potential) for c in get_b30_calculated_list(calculated_list)
    ]
    r10_ptt_list = [
        Decimal(c.potential) for c in get_r10_calculated_list(calculated_list)
    ]
    b30_sum = sum(b30_ptt_list) or Decimal("0.0")
    r10_sum = sum(r10_ptt_list) or Decimal("0.0")
    return (b30_sum + r10_sum) / (len(b30_ptt_list) + len(r10_ptt_list))
