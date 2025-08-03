from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, String
from sqlalchemy.types import TypeDecorator

from arcaea_offline.utils import Version


class ForceTimezoneDateTime(TypeDecorator):
    """
    Store timezone aware timestamps as timezone naive UTC

    https://docs.sqlalchemy.org/en/20/core/custom_types.html#store-timezone-aware-timestamps-as-timezone-naive-utc
    """

    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value: Optional[datetime], dialect):
        if value is not None:
            if not value.tzinfo or value.tzinfo.utcoffset(value) is None:
                raise TypeError("datetime tzinfo is required")
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value: Optional[datetime], dialect):
        if value is not None:
            value = value.replace(tzinfo=timezone.utc)
        return value


class VersionDatabaseType(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: Optional[Version], dialect):
        if value is None:
            return None

        if not isinstance(value, Version):
            raise ValueError("Input is not a Version instance.")

        return str(f"{value.first}.{value.second}.{value.third}")

    def process_result_value(self, value: Optional[str], dialect):
        if value is None:
            return None

        return Version(*(map(int, value.split("."))))
