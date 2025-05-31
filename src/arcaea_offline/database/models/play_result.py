from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Integer, String, Text, Uuid, case, func, inspect, select, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import create_view

from ._base import ModelBase, ModelViewBase, ReprHelper
from .chart_info import ChartInfo
from .difficulty import Difficulty

__all__ = [
    "CalculatedPotential",
    "PlayResult",
    "PlayResultBest",
    "PlayResultCalculated",
]


class PlayResult(ModelBase, ReprHelper):
    __tablename__ = "play_result"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    uuid: Mapped[UUID] = mapped_column(
        Uuid, nullable=False, unique=True, default=lambda: uuid4()
    )
    song_id: Mapped[str] = mapped_column(String)
    rating_class: Mapped[int] = mapped_column(Integer)
    played_at: Mapped[Optional[datetime]] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    score: Mapped[int]
    pure: Mapped[Optional[int]]
    pure_early: Mapped[Optional[int]]
    pure_late: Mapped[Optional[int]]
    far: Mapped[Optional[int]]
    far_early: Mapped[Optional[int]]
    far_late: Mapped[Optional[int]]
    lost: Mapped[Optional[int]]

    max_recall: Mapped[Optional[int]]
    clear_type: Mapped[Optional[int]]
    modifier: Mapped[Optional[int]]
    comment: Mapped[Optional[str]] = mapped_column(Text)


class PlayResultCalculated(ModelViewBase, ReprHelper):
    __tablename__ = "play_results_calculated"

    id: Mapped[int]
    uuid: Mapped[UUID]
    song_id: Mapped[str]
    rating_class: Mapped[int]
    score: Mapped[int]
    pure: Mapped[Optional[int]]
    pure_early: Mapped[Optional[int]]
    pure_late: Mapped[Optional[int]]
    shiny_pure: Mapped[Optional[int]]
    far: Mapped[Optional[int]]
    far_early: Mapped[Optional[int]]
    far_late: Mapped[Optional[int]]
    lost: Mapped[Optional[int]]
    played_at: Mapped[Optional[datetime]]
    max_recall: Mapped[Optional[int]]
    modifier: Mapped[Optional[int]]
    clear_type: Mapped[Optional[int]]
    potential: Mapped[float]
    comment: Mapped[Optional[str]]

    __table__ = create_view(
        name=__tablename__,
        selectable=select(
            PlayResult.id,
            Difficulty.song_id,
            Difficulty.rating_class,
            PlayResult.score,
            PlayResult.pure,
            (
                case(
                    (
                        (
                            ChartInfo.notes.is_not(None)
                            & PlayResult.pure.is_not(None)
                            & PlayResult.far.is_not(None)
                            & (ChartInfo.notes != 0)
                        ),
                        PlayResult.score
                        - func.floor(
                            (PlayResult.pure * 10000000.0 / ChartInfo.notes)
                            + (PlayResult.far * 0.5 * 10000000.0 / ChartInfo.notes)
                        ),
                    ),
                    else_=text("NULL"),
                )
            ).label("shiny_pure"),
            PlayResult.far,
            PlayResult.lost,
            PlayResult.played_at,
            PlayResult.max_recall,
            PlayResult.modifier,
            PlayResult.clear_type,
            case(
                (PlayResult.score >= 10000000, ChartInfo.constant / 10.0 + 2),  # noqa: PLR2004
                (
                    PlayResult.score >= 9800000,  # noqa: PLR2004
                    ChartInfo.constant / 10.0
                    + 1
                    + (PlayResult.score - 9800000) / 200000.0,
                ),
                else_=func.max(
                    (ChartInfo.constant / 10.0)
                    + (PlayResult.score - 9500000) / 300000.0,
                    0,
                ),
            ).label("potential"),
            PlayResult.comment,
        )
        .select_from(Difficulty)
        .join(
            ChartInfo,
            (Difficulty.song_id == ChartInfo.song_id)
            & (Difficulty.rating_class == ChartInfo.rating_class),
        )
        .join(
            PlayResult,
            (Difficulty.song_id == PlayResult.song_id)
            & (Difficulty.rating_class == PlayResult.rating_class),
        ),
        metadata=ModelViewBase.metadata,
        cascade_on_drop=False,
    )


class PlayResultBest(ModelViewBase, ReprHelper):
    __tablename__ = "play_results_best"

    id: Mapped[int]
    uuid: Mapped[UUID]
    song_id: Mapped[str]
    rating_class: Mapped[int]
    score: Mapped[int]
    pure: Mapped[Optional[int]]
    pure_early: Mapped[Optional[int]]
    pure_late: Mapped[Optional[int]]
    shiny_pure: Mapped[Optional[int]]
    far: Mapped[Optional[int]]
    far_early: Mapped[Optional[int]]
    far_late: Mapped[Optional[int]]
    lost: Mapped[Optional[int]]
    played_at: Mapped[Optional[datetime]]
    max_recall: Mapped[Optional[int]]
    modifier: Mapped[Optional[int]]
    clear_type: Mapped[Optional[int]]
    potential: Mapped[float]
    comment: Mapped[Optional[str]]

    __table__ = create_view(
        name=__tablename__,
        selectable=select(
            *[
                col
                for col in inspect(PlayResultCalculated).columns
                if col.name != "potential"
            ],
            func.max(PlayResultCalculated.potential).label("potential"),
        )
        .select_from(PlayResultCalculated)
        .group_by(PlayResultCalculated.song_id, PlayResultCalculated.rating_class)
        .order_by(PlayResultCalculated.potential.desc()),
        metadata=ModelViewBase.metadata,
        cascade_on_drop=False,
    )


class CalculatedPotential(ModelViewBase, ReprHelper):
    __tablename__ = "calculated_potential"

    b30: Mapped[float]

    _select_bests_subquery = (
        select(PlayResultBest.potential.label("b30_sum"))
        .order_by(PlayResultBest.potential.desc())
        .limit(30)
        .subquery()
    )
    __table__ = create_view(
        name=__tablename__,
        selectable=select(func.avg(_select_bests_subquery.c.b30_sum).label("b30")),
        metadata=ModelViewBase.metadata,
        cascade_on_drop=False,
    )
