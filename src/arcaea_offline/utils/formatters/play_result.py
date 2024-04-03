from typing import Any, Literal, overload

from arcaea_offline.constants.enums import (
    ArcaeaPlayResultClearType,
    ArcaeaPlayResultModifier,
)
from arcaea_offline.constants.play_result import ScoreLowerLimits


class PlayResultFormatter:
    SCORE_GRADE_FORMAT_RESULTS = Literal["EX+", "EX", "AA", "A", "B", "C", "D"]

    @staticmethod
    def score_grade(score: int) -> SCORE_GRADE_FORMAT_RESULTS:
        """
        Returns the score grade, e.g. EX+.

        Raises `ValueError` if the score is negative.
        """
        if not isinstance(score, int):
            raise TypeError(f"Unsupported type {type(score)}, cannot format")

        if score >= ScoreLowerLimits.EX_PLUS:
            return "EX+"
        elif score >= ScoreLowerLimits.EX:
            return "EX"
        elif score >= ScoreLowerLimits.AA:
            return "AA"
        elif score >= ScoreLowerLimits.A:
            return "A"
        elif score >= ScoreLowerLimits.B:
            return "B"
        elif score >= ScoreLowerLimits.C:
            return "C"
        elif score >= ScoreLowerLimits.D:
            return "D"
        else:
            raise ValueError("score cannot be negative")

    CLEAR_TYPE_FORMAT_RESULTS = Literal[
        "TRACK LOST",
        "NORMAL CLEAR",
        "FULL RECALL",
        "PURE MEMORY",
        "EASY CLEAR",
        "HARD CLEAR",
        "UNKNOWN",
        "None",
    ]

    @overload
    @classmethod
    def clear_type(
        cls, clear_type: ArcaeaPlayResultClearType
    ) -> CLEAR_TYPE_FORMAT_RESULTS:
        """
        Returns the uppercased clear type name, e.g. NORMAL CLEAR.
        """
        ...

    @overload
    @classmethod
    def clear_type(cls, clear_type: int) -> CLEAR_TYPE_FORMAT_RESULTS:
        """
        Returns the uppercased clear type name, e.g. NORMAL CLEAR.

        The integer will be converted to `ArcaeaPlayResultClearType` enum,
        and will return "UNKNOWN" if the convertion fails.

        Raises `ValueError` if the integer is negative.
        """
        ...

    @overload
    @classmethod
    def clear_type(cls, clear_type: None) -> CLEAR_TYPE_FORMAT_RESULTS:
        """
        Returns "None"
        """
        ...

    @classmethod
    def clear_type(cls, clear_type: Any) -> CLEAR_TYPE_FORMAT_RESULTS:
        if clear_type is None:
            return "None"
        elif isinstance(clear_type, ArcaeaPlayResultClearType):
            return clear_type.name.replace("_", " ").upper()  # type: ignore
        elif isinstance(clear_type, int):
            if clear_type < 0:
                raise ValueError("clear_type cannot be negative")
            try:
                return cls.clear_type(ArcaeaPlayResultClearType(clear_type))
            except ValueError:
                return "UNKNOWN"
        else:
            raise TypeError(f"Unsupported type {type(clear_type)}, cannot format")

    MODIFIER_FORMAT_RESULTS = Literal["NORMAL", "EASY", "HARD", "UNKNOWN", "None"]

    @overload
    @classmethod
    def modifier(cls, modifier: ArcaeaPlayResultModifier) -> MODIFIER_FORMAT_RESULTS:
        """
        Returns the uppercased clear type name, e.g. NORMAL CLEAR.
        """
        ...

    @overload
    @classmethod
    def modifier(cls, modifier: int) -> MODIFIER_FORMAT_RESULTS:
        """
        Returns the uppercased clear type name, e.g. NORMAL CLEAR.

        The integer will be converted to `ArcaeaPlayResultModifier` enum,
        and will return "UNKNOWN" if the convertion fails.

        Raises `ValueError` if the integer is negative.
        """
        ...

    @overload
    @classmethod
    def modifier(cls, modifier: None) -> MODIFIER_FORMAT_RESULTS:
        """
        Returns "None"
        """
        ...

    @classmethod
    def modifier(cls, modifier: Any) -> MODIFIER_FORMAT_RESULTS:
        if modifier is None:
            return "None"
        elif isinstance(modifier, ArcaeaPlayResultModifier):
            return modifier.name
        elif isinstance(modifier, int):
            if modifier < 0:
                raise ValueError("modifier cannot be negative")
            try:
                return cls.modifier(ArcaeaPlayResultModifier(modifier))
            except ValueError:
                return "UNKNOWN"
        else:
            raise TypeError(f"Unsupported type {type(modifier)}, cannot format")
