# pylint: disable=too-few-public-methods

from sqlalchemy import TEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .common import ReprHelper

__all__ = [
    "ConfigBase",
    "Property",
]


class ConfigBase(DeclarativeBase, ReprHelper):
    pass


class Property(ConfigBase):
    __tablename__ = "properties"

    key: Mapped[str] = mapped_column(TEXT(), primary_key=True)
    value: Mapped[str] = mapped_column(TEXT())
