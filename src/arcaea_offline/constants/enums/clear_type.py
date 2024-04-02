from enum import IntEnum


class ArcaeaScoreClearType(IntEnum):
    TRACK_LOST = 0
    NORMAL_CLEAR = 1
    FULL_RECALL = 2
    PURE_MEMORY = 3
    HARD_CLEAR = 4
    EASY_CLEAR = 5
