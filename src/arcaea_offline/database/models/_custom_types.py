from datetime import datetime, timezone
from enum import IntEnum
from typing import Optional, Type

from sqlalchemy import DateTime, Integer
from sqlalchemy.types import TypeDecorator


class DbIntEnum(TypeDecorator):
    """sqlalchemy `TypeDecorator` for `IntEnum`s"""

    impl = Integer
    cache_ok = True

    def __init__(self, enum_class: Type[IntEnum]):
        super().__init__()
        self.enum_class = enum_class

    def process_bind_param(self, value: Optional[IntEnum], dialect) -> Optional[int]:
        return None if value is None else value.value

    def process_result_value(self, value: Optional[int], dialect) -> Optional[IntEnum]:
        return None if value is None else self.enum_class(value)


class TZDateTime(TypeDecorator):
    """
    Store Timezone Aware Timestamps as Timezone Naive UTC

    https://docs.sqlalchemy.org/en/20/core/custom_types.html#store-timezone-aware-timestamps-as-timezone-naive-utc
    """

    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value: Optional[datetime], dialect):
        if value is not None:
            if not value.tzinfo or value.tzinfo.utcoffset(value) is None:
                raise TypeError("tzinfo is required")
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value: Optional[datetime], dialect):
        if value is not None:
            value = value.replace(tzinfo=timezone.utc)
        return value
