from sqlalchemy.orm import Mapped, mapped_column

from ._base import ModelBase, ReprHelper

__all__ = ["Property"]


class Property(ModelBase, ReprHelper):
    __tablename__ = "property"

    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column()
