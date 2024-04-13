from typing import Optional

from sqlalchemy import Integer
from sqlalchemy.types import TypeDecorator

from arcaea_offline.constants.enums import (
    ArcaeaPlayResultClearType,
    ArcaeaPlayResultModifier,
    ArcaeaRatingClass,
)


class DbRatingClass(TypeDecorator):
    """sqlalchemy rating_class type decorator"""

    impl = Integer

    def process_bind_param(
        self, value: Optional[ArcaeaRatingClass], dialect
    ) -> Optional[int]:
        return None if value is None else value.value

    def process_result_value(
        self, value: Optional[int], dialect
    ) -> Optional[ArcaeaRatingClass]:
        return None if value is None else ArcaeaRatingClass(value)


class DbClearType(TypeDecorator):
    """sqlalchemy clear_type type decorator"""

    impl = Integer

    def process_bind_param(
        self, value: Optional[ArcaeaPlayResultClearType], dialect
    ) -> Optional[int]:
        return None if value is None else value.value

    def process_result_value(
        self, value: Optional[int], dialect
    ) -> Optional[ArcaeaPlayResultClearType]:
        return None if value is None else ArcaeaPlayResultClearType(value)


class DbModifier(TypeDecorator):
    """sqlalchemy modifier type decorator"""

    impl = Integer

    def process_bind_param(
        self, value: Optional[ArcaeaPlayResultModifier], dialect
    ) -> Optional[int]:
        return None if value is None else value.value

    def process_result_value(
        self, value: Optional[int], dialect
    ) -> Optional[ArcaeaPlayResultModifier]:
        return None if value is None else ArcaeaPlayResultModifier(value)
