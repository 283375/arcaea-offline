from typing import Optional

RATING_CLASS_TEXT_MAP = {
    0: "Past",
    1: "Present",
    2: "Future",
    3: "Beyond",
    4: "Eternal",
}

RATING_CLASS_SHORT_TEXT_MAP = {
    0: "PST",
    1: "PRS",
    2: "FTR",
    3: "BYD",
    4: "ETR",
}


def rating_class_to_text(rating_class: int) -> Optional[str]:
    return RATING_CLASS_TEXT_MAP.get(rating_class)


def rating_class_to_short_text(rating_class: int) -> Optional[str]:
    return RATING_CLASS_SHORT_TEXT_MAP.get(rating_class)
