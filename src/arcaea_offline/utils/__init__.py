from typing import Any, Optional, Sequence

RATING_CLASS_TEXT_MAP = {
    0: "Past",
    1: "Present",
    2: "Future",
    3: "Beyond",
}

RATING_CLASS_SHORT_TEXT_MAP = {
    0: "PST",
    1: "PRS",
    2: "FTR",
    3: "BYD",
}


def rating_class_to_text(rating_class: int) -> Optional[str]:
    return RATING_CLASS_TEXT_MAP.get(rating_class)


def rating_class_to_short_text(rating_class: int) -> Optional[str]:
    return RATING_CLASS_SHORT_TEXT_MAP.get(rating_class)


SCORE_GRADE_FLOOR = [9900000, 9800000, 9500000, 9200000, 8900000, 8600000, 0]
SCORE_GRADE_TEXTS = ["EX+", "EX", "AA", "A", "B", "C", "D"]


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
