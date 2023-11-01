# pylint: disable=too-few-public-methods, duplicate-code

from typing import Optional

from sqlalchemy import TEXT, case, func, inspect, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy_utils import create_view

from .common import ReprHelper
from .songs import ChartInfo, Difficulty

__all__ = [
    "ScoresBase",
    "Score",
    "ScoresViewBase",
    "ScoreCalculated",
    "ScoreBest",
    "CalculatedPotential",
]


class ScoresBase(DeclarativeBase, ReprHelper):
    pass


class Score(ScoresBase):
    __tablename__ = "scores"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    song_id: Mapped[str] = mapped_column(TEXT())
    rating_class: Mapped[int]
    score: Mapped[int]
    pure: Mapped[Optional[int]]
    far: Mapped[Optional[int]]
    lost: Mapped[Optional[int]]
    date: Mapped[Optional[int]]
    max_recall: Mapped[Optional[int]]
    modifier: Mapped[Optional[int]] = mapped_column(
        comment="0: NORMAL, 1: EASY, 2: HARD"
    )
    clear_type: Mapped[Optional[int]] = mapped_column(
        comment="0: TRACK LOST, 1: NORMAL CLEAR, 2: FULL RECALL, "
        "3: PURE MEMORY, 4: EASY CLEAR, 5: HARD CLEAR"
    )
    comment: Mapped[Optional[str]] = mapped_column(TEXT())


# How to create an SQL View with SQLAlchemy?
# https://stackoverflow.com/a/53253105/16484891
# CC BY-SA 4.0


class ScoresViewBase(DeclarativeBase, ReprHelper):
    pass


class ScoreCalculated(ScoresViewBase):
    __tablename__ = "scores_calculated"

    id: Mapped[int]
    song_id: Mapped[str]
    rating_class: Mapped[int]
    score: Mapped[int]
    pure: Mapped[Optional[int]]
    shiny_pure: Mapped[Optional[int]]
    far: Mapped[Optional[int]]
    lost: Mapped[Optional[int]]
    date: Mapped[Optional[int]]
    max_recall: Mapped[Optional[int]]
    modifier: Mapped[Optional[int]]
    clear_type: Mapped[Optional[int]]
    potential: Mapped[float]
    comment: Mapped[Optional[str]]

    __table__ = create_view(
        name=__tablename__,
        selectable=select(
            Score.id,
            Difficulty.song_id,
            Difficulty.rating_class,
            Score.score,
            Score.pure,
            (
                case(
                    (
                        (
                            ChartInfo.notes.is_not(None)
                            & Score.pure.is_not(None)
                            & Score.far.is_not(None)
                            & (ChartInfo.notes != 0)
                        ),
                        Score.score
                        - func.floor(
                            (Score.pure * 10000000.0 / ChartInfo.notes)
                            + (Score.far * 0.5 * 10000000.0 / ChartInfo.notes)
                        ),
                    ),
                    else_=text("NULL"),
                )
            ).label("shiny_pure"),
            Score.far,
            Score.lost,
            Score.date,
            Score.max_recall,
            Score.modifier,
            Score.clear_type,
            case(
                (Score.score >= 10000000, ChartInfo.constant / 10.0 + 2),
                (
                    Score.score >= 9800000,
                    ChartInfo.constant / 10.0 + 1 + (Score.score - 9800000) / 200000.0,
                ),
                else_=func.max(
                    (ChartInfo.constant / 10.0) + (Score.score - 9500000) / 300000.0,
                    0,
                ),
            ).label("potential"),
            Score.comment,
        )
        .select_from(Difficulty)
        .join(
            ChartInfo,
            (Difficulty.song_id == ChartInfo.song_id)
            & (Difficulty.rating_class == ChartInfo.rating_class),
        )
        .join(
            Score,
            (Difficulty.song_id == Score.song_id)
            & (Difficulty.rating_class == Score.rating_class),
        ),
        metadata=ScoresViewBase.metadata,
        cascade_on_drop=False,
    )


class ScoreBest(ScoresViewBase):
    __tablename__ = "scores_best"

    id: Mapped[int]
    song_id: Mapped[str]
    rating_class: Mapped[int]
    score: Mapped[int]
    pure: Mapped[Optional[int]]
    shiny_pure: Mapped[Optional[int]]
    far: Mapped[Optional[int]]
    lost: Mapped[Optional[int]]
    date: Mapped[Optional[int]]
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
                for col in inspect(ScoreCalculated).columns
                if col.name != "potential"
            ],
            func.max(ScoreCalculated.potential).label("potential"),
        )
        .select_from(ScoreCalculated)
        .group_by(ScoreCalculated.song_id, ScoreCalculated.rating_class)
        .order_by(ScoreCalculated.potential.desc()),
        metadata=ScoresViewBase.metadata,
        cascade_on_drop=False,
    )


class CalculatedPotential(ScoresViewBase):
    __tablename__ = "calculated_potential"

    b30: Mapped[float]

    _select_bests_subquery = (
        select(ScoreBest.potential.label("b30_sum"))
        .order_by(ScoreBest.potential.desc())
        .limit(30)
        .subquery()
    )
    __table__ = create_view(
        name=__tablename__,
        selectable=select(func.avg(_select_bests_subquery.c.b30_sum).label("b30")),
        metadata=ScoresViewBase.metadata,
        cascade_on_drop=False,
    )
