from sqlalchemy import TEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

__all__ = [
    "CommonBase",
    "Property",
]


class CommonBase(DeclarativeBase):
    pass


class Property(CommonBase):
    __tablename__ = "property"

    key: Mapped[str] = mapped_column(TEXT(), primary_key=True)
    value: Mapped[str] = mapped_column(TEXT())
