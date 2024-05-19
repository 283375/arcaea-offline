from enum import Enum, IntEnum


class ArcaeaRatingClass(IntEnum):
    PAST = 0
    PRESENT = 1
    FUTURE = 2
    BEYOND = 3
    ETERNAL = 4


class ArcaeaSongSide(IntEnum):
    LIGHT = 0
    CONFLICT = 1
    COLORLESS = 2


class ArcaeaPlayResultModifier(IntEnum):
    NORMAL = 0
    EASY = 1
    HARD = 2


class ArcaeaPlayResultClearType(IntEnum):
    TRACK_LOST = 0
    NORMAL_CLEAR = 1
    FULL_RECALL = 2
    PURE_MEMORY = 3
    HARD_CLEAR = 4
    EASY_CLEAR = 5


class ArcaeaLanguage(Enum):
    JA = "ja"
    KO = "ko"
    ZH_HANT = "zh-Hant"
    ZH_HANS = "zh-Hans"
