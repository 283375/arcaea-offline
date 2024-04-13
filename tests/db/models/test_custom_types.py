from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from arcaea_offline.constants.enums import (
    ArcaeaPlayResultClearType,
    ArcaeaPlayResultModifier,
    ArcaeaRatingClass,
)
from arcaea_offline.database.models._custom_types import (
    DbClearType,
    DbModifier,
    DbRatingClass,
)


class Base(DeclarativeBase):
    pass


class RatingClassTestModel(Base):
    __tablename__ = "test_rating_class"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[Optional[ArcaeaRatingClass]] = mapped_column(
        DbRatingClass, nullable=True
    )


class ClearTypeTestModel(Base):
    __tablename__ = "test_clear_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[Optional[ArcaeaPlayResultClearType]] = mapped_column(
        DbClearType, nullable=True
    )


class ModifierTestModel(Base):
    __tablename__ = "test_modifier"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[Optional[ArcaeaPlayResultModifier]] = mapped_column(
        DbModifier, nullable=True
    )


class TestCustomTypes:
    def _common_test_method(self, db_session, obj: Base, value_in_db):
        """
        This method stores the `obj` into the given `db_session`,
        then fetches the raw value of `obj.value` from database,
        and asserts that the value is equal to `value_in_db`.
        """
        db_session.add(obj)
        db_session.commit()

        exec_result = db_session.execute(
            text(
                f"SELECT value FROM {obj.__tablename__} WHERE id = {obj.id}"  # type: ignore
            )
        ).fetchone()[0]

        if value_in_db is None:
            assert exec_result is value_in_db
        else:
            assert exec_result == value_in_db

    def test_rating_class(self, db_session):
        Base.metadata.create_all(db_session.bind)

        basic_obj = RatingClassTestModel(id=1, value=ArcaeaRatingClass.FUTURE)
        self._common_test_method(db_session, basic_obj, 2)

        null_obj = RatingClassTestModel(id=2, value=None)
        self._common_test_method(db_session, null_obj, None)

    def test_clear_type(self, db_session):
        Base.metadata.create_all(db_session.bind)

        basic_obj = ClearTypeTestModel(id=1, value=ArcaeaPlayResultClearType.TRACK_LOST)
        self._common_test_method(db_session, basic_obj, 0)

        null_obj = ClearTypeTestModel(id=2, value=None)
        self._common_test_method(db_session, null_obj, None)

    def test_modifier(self, db_session):
        Base.metadata.create_all(db_session.bind)

        basic_obj = ModifierTestModel(id=1, value=ArcaeaPlayResultModifier.HARD)
        self._common_test_method(db_session, basic_obj, 2)

        null_obj = ModifierTestModel(id=2, value=None)
        self._common_test_method(db_session, null_obj, None)
