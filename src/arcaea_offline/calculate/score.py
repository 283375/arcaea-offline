from decimal import Decimal
from math import floor


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
