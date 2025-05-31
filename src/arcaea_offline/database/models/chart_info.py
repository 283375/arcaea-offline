from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKeyConstraint, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import ModelBase, ReprHelper
from ._types import ForceTimezoneDateTime

if TYPE_CHECKING:
    from .difficulty import Difficulty


class ChartInfo(ModelBase, ReprHelper):
    __tablename__ = "chart_info"
    __table_args__ = (
        ForeignKeyConstraint(
            ["song_id", "rating_class"],
            ["difficulty.song_id", "difficulty.rating_class"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )

    difficulty: Mapped["Difficulty"] = relationship(back_populates="chart_info_list")

    song_id: Mapped[str] = mapped_column(String, primary_key=True)
    rating_class: Mapped[int] = mapped_column(Integer, primary_key=True)
    constant: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    notes: Mapped[int] = mapped_column(Integer)
    added_at: Mapped[datetime] = mapped_column(ForceTimezoneDateTime, primary_key=True)
    version: Mapped[Optional[str]] = mapped_column(String)
