from datetime import datetime
from enum import IntEnum


class KanaeDayNight(IntEnum):
    DAY = 0
    NIGHT = 1

    @staticmethod
    def from_datetime(dt: datetime) -> "KanaeDayNight":
        return KanaeDayNight.DAY if 6 <= dt.hour <= 19 else KanaeDayNight.NIGHT  # noqa: PLR2004
