from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.exc import DetachedInstanceError

from arcaea_offline.constants.enums import (
    ArcaeaPlayResultClearType,
    ArcaeaPlayResultModifier,
    ArcaeaRatingClass,
    ArcaeaSongSide,
)

from ._custom_types import DbIntEnum, TZDateTime

TYPE_ANNOTATION_MAP = {
    datetime: TZDateTime,
    ArcaeaRatingClass: DbIntEnum(ArcaeaRatingClass),
    ArcaeaSongSide: DbIntEnum(ArcaeaSongSide),
    ArcaeaPlayResultClearType: DbIntEnum(ArcaeaPlayResultClearType),
    ArcaeaPlayResultModifier: DbIntEnum(ArcaeaPlayResultModifier),
}


class ModelsV5Base(DeclarativeBase):
    type_annotation_map = TYPE_ANNOTATION_MAP


class ModelsV5ViewBase(DeclarativeBase):
    type_annotation_map = TYPE_ANNOTATION_MAP


class ReprHelper:
    # pylint: disable=no-member

    def _repr(self, **kwargs) -> str:
        """
        Helper for __repr__

        https://stackoverflow.com/a/55749579/16484891

        CC BY-SA 4.0
        """
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in kwargs.items():
            try:
                field_strings.append(f"{key}={field!r}")
            except DetachedInstanceError:
                field_strings.append(f"{key}=DetachedInstanceError")
            else:
                at_least_one_attached_attribute = True

        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({', '.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __repr__(self):
        if isinstance(self, DeclarativeBase):
            return self._repr(
                **{c.key: getattr(self, c.key) for c in self.__table__.columns}
            )
        return super().__repr__()
