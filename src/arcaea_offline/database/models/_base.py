from datetime import datetime

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.exc import DetachedInstanceError

from ._types import ForceTimezoneDateTime

TYPE_ANNOTATION_MAP = {
    datetime: ForceTimezoneDateTime,
}


class ModelBase(DeclarativeBase):
    type_annotation_map = TYPE_ANNOTATION_MAP
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class ModelViewBase(DeclarativeBase):
    type_annotation_map = TYPE_ANNOTATION_MAP


class ReprHelper:
    # pylint: disable=no-member

    def _repr(self, **kwargs) -> str:
        """
        SQLAlchemy model __repr__ helper

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
