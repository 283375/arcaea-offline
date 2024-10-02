from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import ForeignKey, and_, case, func, inspect, select, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import create_view

from arcaea_offline.constants.enums import (
    ArcaeaPlayResultClearType,
    ArcaeaPlayResultModifier,
    ArcaeaRatingClass,
)

from .arcaea import ChartInfo, Difficulty
from .base import ModelsV5Base, ModelsV5ViewBase, ReprHelper

__all__ = [
    "CalculatedPotential",
    "PlayResult",
    "PlayResultBest",
    "PlayResultCalculated",
]


class PlayResult(ModelsV5Base, ReprHelper):
    __tablename__ = "play_results"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    song_id: Mapped[str] = mapped_column(
        ForeignKey(Difficulty.song_id, onupdate="CASCADE", ondelete="NO ACTION"),
        index=True,
    )
    rating_class: Mapped[ArcaeaRatingClass] = mapped_column(
        ForeignKey(Difficulty.rating_class, onupdate="CASCADE", ondelete="NO ACTION"),
        index=True,
    )
    score: Mapped[int]
    pure: Mapped[Optional[int]]
    far: Mapped[Optional[int]]
    lost: Mapped[Optional[int]]
    date: Mapped[Optional[datetime]] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    max_recall: Mapped[Optional[int]]
    modifier: Mapped[Optional[ArcaeaPlayResultModifier]]
    clear_type: Mapped[Optional[ArcaeaPlayResultClearType]]
    comment: Mapped[Optional[str]]

    difficulty: Mapped[Difficulty] = relationship(
        primaryjoin=and_(
            song_id == Difficulty.song_id,
            rating_class == Difficulty.rating_class,
        ),
        viewonly=True,
    )


# How to create an SQL View with SQLAlchemy?
# https://stackoverflow.com/a/53253105/16484891
# CC BY-SA 4.0


class PlayResultCalculated(ModelsV5ViewBase, ReprHelper):
    __tablename__ = "play_results_calculated"

    id: Mapped[int]
    song_id: Mapped[str]
    rating_class: Mapped[ArcaeaRatingClass]
    score: Mapped[int]
    pure: Mapped[Optional[int]]
    shiny_pure: Mapped[Optional[int]]
    far: Mapped[Optional[int]]
    lost: Mapped[Optional[int]]
    date: Mapped[Optional[datetime]]
    max_recall: Mapped[Optional[int]]
    modifier: Mapped[Optional[ArcaeaPlayResultModifier]]
    clear_type: Mapped[Optional[ArcaeaPlayResultClearType]]
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
            PlayResult.date,
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
        metadata=ModelsV5ViewBase.metadata,
        cascade_on_drop=False,
    )


class PlayResultBest(ModelsV5ViewBase, ReprHelper):
    __tablename__ = "play_results_best"

    id: Mapped[int]
    song_id: Mapped[str]
    rating_class: Mapped[ArcaeaRatingClass]
    score: Mapped[int]
    pure: Mapped[Optional[int]]
    shiny_pure: Mapped[Optional[int]]
    far: Mapped[Optional[int]]
    lost: Mapped[Optional[int]]
    date: Mapped[Optional[datetime]]
    max_recall: Mapped[Optional[int]]
    modifier: Mapped[Optional[ArcaeaPlayResultModifier]]
    clear_type: Mapped[Optional[ArcaeaPlayResultClearType]]
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
        metadata=ModelsV5ViewBase.metadata,
        cascade_on_drop=False,
    )


class CalculatedPotential(ModelsV5ViewBase, ReprHelper):
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
        metadata=ModelsV5ViewBase.metadata,
        cascade_on_drop=False,
    )
