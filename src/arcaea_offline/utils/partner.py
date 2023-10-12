from datetime import datetime
from enum import IntEnum


class KanaeDayNight(IntEnum):
    Day = 0
    Night = 1


def kanae_day_night(timestamp: int) -> KanaeDayNight:
    """
    :param timestamp: POSIX timestamp, which is passed to `datetime.fromtimestamp(timestamp)`.
    """
    dt = datetime.fromtimestamp(timestamp)
    return KanaeDayNight.Day if 6 <= dt.hour <= 19 else KanaeDayNight.Night
