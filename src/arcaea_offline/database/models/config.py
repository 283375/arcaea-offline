from sqlalchemy.orm import Mapped, mapped_column

from .base import ModelsV5Base, ReprHelper

__all__ = ["Property"]


class Property(ModelsV5Base, ReprHelper):
    __tablename__ = "properties"

    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column()
