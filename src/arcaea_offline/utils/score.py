from typing import Any, Sequence

SCORE_GRADE_FLOOR = [9900000, 9800000, 9500000, 9200000, 8900000, 8600000, 0]
SCORE_GRADE_TEXTS = ["EX+", "EX", "AA", "A", "B", "C", "D"]
MODIFIER_TEXTS = ["NORMAL", "EASY", "HARD"]
CLEAR_TYPE_TEXTS = [
    "TRACK LOST",
    "NORMAL CLEAR",
    "FULL RECALL",
    "PURE MEMORY",
    "EASY CLEAR",
    "HARD CLEAR",
]


def zip_score_grade(score: int, __seq: Sequence, default: Any = "__PRESERVE__"):
    """
    zip_score_grade is a simple wrapper that equals to:
    ```py
    for score_floor, val in zip(SCORE_GRADE_FLOOR, __seq):
        if score >= score_floor:
            return val
    return seq[-1] if default == "__PRESERVE__" else default
    ```
    Could be useful in specific cases.
    """
    return next(
        (
            val
            for score_floor, val in zip(SCORE_GRADE_FLOOR, __seq)
            if score >= score_floor
        ),
        __seq[-1] if default == "__PRESERVE__" else default,
    )


def score_to_grade_text(score: int) -> str:
    return zip_score_grade(score, SCORE_GRADE_TEXTS)


def modifier_to_text(modifier: int) -> str:
    return MODIFIER_TEXTS[modifier]


def clear_type_to_text(clear_type: int) -> str:
    return CLEAR_TYPE_TEXTS[clear_type]
