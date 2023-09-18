from dataclasses import dataclass
from decimal import Decimal
from math import floor
from typing import Tuple, Union


def calculate_score_range(notes: int, pure: int, far: int):
    single_note_score = 10000000 / Decimal(notes)

    actual_score = floor(
        single_note_score * pure + single_note_score * Decimal(0.5) * far
    )
    return (actual_score, actual_score + pure)


def calculate_score_modifier(score: int) -> Decimal:
    if score >= 10000000:
        return Decimal(2)
    elif score >= 9800000:
        return Decimal(1) + (Decimal(score - 9800000) / 200000)
    else:
        return Decimal(score - 9500000) / 300000


def calculate_play_rating(
    constant: Union[Decimal, str, float, int], score: int
) -> Decimal:
    constant = Decimal(constant)
    score_modifier = calculate_score_modifier(score)
    return max(Decimal(0), constant + score_modifier)


def calculate_shiny_pure(notes: int, score: int, pure: int, far: int) -> int:
    single_note_score = 10000000 / Decimal(notes)
    actual_score = single_note_score * pure + single_note_score * Decimal(0.5) * far
    return score - floor(actual_score)


@dataclass
class ConstantsFromPlayRatingResult:
    EXPlus: Tuple[Decimal, Decimal]
    EX: Tuple[Decimal, Decimal]
    AA: Tuple[Decimal, Decimal]
    A: Tuple[Decimal, Decimal]
    B: Tuple[Decimal, Decimal]
    C: Tuple[Decimal, Decimal]


def calculate_constants_from_play_rating(play_rating: Union[Decimal, str, float, int]):
    play_rating = Decimal(play_rating)

    ranges = []
    for upperScore, lowerScore in [
        (10000000, 9900000),
        (9899999, 9800000),
        (9799999, 9500000),
        (9499999, 9200000),
        (9199999, 8900000),
        (8899999, 8600000),
    ]:
        upperScoreModifier = calculate_score_modifier(upperScore)
        lowerScoreModifier = calculate_score_modifier(lowerScore)
        ranges.append(
            (play_rating - upperScoreModifier, play_rating - lowerScoreModifier)
        )

    return ConstantsFromPlayRatingResult(*ranges)
