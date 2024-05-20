from datetime import datetime, timedelta, timezone
from enum import IntEnum
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from arcaea_offline.database.models._custom_types import DbIntEnum, TZDateTime


class TestIntEnum(IntEnum):
    __test__ = False

    ONE = 1
    TWO = 2
    THREE = 3


class TestBase(DeclarativeBase):
    __test__ = False

    id: Mapped[int] = mapped_column(primary_key=True)


class IntEnumTestModel(TestBase):
    __tablename__ = "test_int_enum"
    value: Mapped[Optional[TestIntEnum]] = mapped_column(DbIntEnum(TestIntEnum))


class TZDatetimeTestModel(TestBase):
    __tablename__ = "test_tz_datetime"
    value: Mapped[Optional[datetime]] = mapped_column(TZDateTime)


class TestCustomTypes:
    def test_int_enum(self, db_session):
        def _query_value(_id: int):
            return db_session.execute(
                text(
                    f"SELECT value FROM {IntEnumTestModel.__tablename__} WHERE id = {_id}"
                )
            ).one()[0]

        TestBase.metadata.create_all(db_session.bind)

        basic_obj = IntEnumTestModel(id=1, value=TestIntEnum.TWO)
        null_obj = IntEnumTestModel(id=2, value=None)
        db_session.add(basic_obj)
        db_session.add(null_obj)
        db_session.commit()

        assert _query_value(1) == TestIntEnum.TWO.value
        assert _query_value(2) is None

    def test_tz_datetime(self, db_session):
        TestBase.metadata.create_all(db_session.bind)

        dt1 = datetime.now(tz=timezone(timedelta(hours=8)))

        basic_obj = TZDatetimeTestModel(id=1, value=dt1)
        null_obj = TZDatetimeTestModel(id=2, value=None)
        db_session.add(basic_obj)
        db_session.add(null_obj)
        db_session.commit()

        assert basic_obj.value == dt1
        assert null_obj.value is None
