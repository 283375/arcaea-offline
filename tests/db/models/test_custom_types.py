from datetime import datetime, timedelta, timezone
from enum import IntEnum
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from arcaea_offline.database.models._types import ForceTimezoneDateTime


class TestIntEnum(IntEnum):
    __test__ = False

    ONE = 1
    TWO = 2
    THREE = 3


class TestBase(DeclarativeBase):
    __test__ = False

    id: Mapped[int] = mapped_column(primary_key=True)


class ForceTimezoneDatetimeTestModel(TestBase):
    __tablename__ = "test_tz_datetime"
    value: Mapped[Optional[datetime]] = mapped_column(ForceTimezoneDateTime)


class TestCustomTypes:
    def test_force_timezone_datetime(self, db_session):
        TestBase.metadata.create_all(db_session.bind, checkfirst=False)

        dt1 = datetime.now(tz=timezone(timedelta(hours=8)))

        basic_obj = ForceTimezoneDatetimeTestModel(id=1, value=dt1)
        null_obj = ForceTimezoneDatetimeTestModel(id=2, value=None)
        db_session.add(basic_obj)
        db_session.add(null_obj)
        db_session.commit()

        assert basic_obj.value == dt1
        assert null_obj.value is None
