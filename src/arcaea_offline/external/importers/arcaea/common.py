from typing import Union


def fix_timestamp(timestamp: int) -> Union[int, None]:
    """
    Some of the `date` column in st3 are unexpectedly truncated. For example,
    a `1670283375` may be truncated to `167028`, even a single `1`.

    To properly handle this:

    If `timestamp > 1489017600` (the release date of Arcaea), consider it's ok.

    Otherwise, if the timestamp is 'fixable'
    (`1489 <= timestamp <= 9999` or `timestamp > 14889`),
    pad zeros to the end of timestamp.
    For example, a `1566` will be padded to `1566000000`.

    Otherwise, treat the timestamp as `None`.

    :param timestamp: `date` value
    """
    if timestamp > 1489017600:  # noqa: PLR2004
        return timestamp

    timestamp_fixable = 1489 <= timestamp <= 9999 or timestamp > 14889  # noqa: PLR2004
    if not timestamp_fixable:
        return None

    timestamp_str = str(timestamp)
    timestamp_str = timestamp_str.ljust(10, "0")
    return int(timestamp_str, 10)
