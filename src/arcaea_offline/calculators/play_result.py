from decimal import Decimal
from math import floor
from typing import Tuple, TypedDict, Union

from arcaea_offline.constants.play_result import ScoreLowerLimits


class PlayResultCalculators:
    @staticmethod
    def score_possible_range(notes: int, pure: int, far: int) -> tuple[int, int]:
        """
        Returns the possible range of score based on the given values.

        The first integer of returned tuple is the lower limit of the score,
        and the second integer is the upper limit.

        For example, ...
        """
        single_note_score = 10000000 / Decimal(notes)

        actual_score = floor(
            single_note_score * pure + single_note_score * Decimal(0.5) * far
        )
        return (actual_score, actual_score + pure)

    @staticmethod
    def shiny_pure(notes: int, score: int, pure: int, far: int) -> int:
        single_note_score = 10000000 / Decimal(notes)
        actual_score = single_note_score * pure + single_note_score * Decimal(0.5) * far
        return score - floor(actual_score)

    @staticmethod
    def score_modifier(score: int) -> Decimal:
        """
        Returns the score modifier of the given score

        https://arcaea.fandom.com/wiki/Potential#Score_Modifier

        :param score: The score of the play result, e.g. 9900000
        :return: The modifier of the given score, e.g. Decimal("1.5")
        """
        if not isinstance(score, int):
            raise TypeError("score must be an integer")
        if score < 0:
            raise ValueError("score cannot be negative")

        if score >= 10000000:
            return Decimal(2)
        if score >= 9800000:
            return Decimal(1) + (Decimal(score - 9800000) / 200000)
        return Decimal(score - 9500000) / 300000

    @classmethod
    def play_rating(cls, score: int, constant: int) -> Decimal:
        """
        Returns the play rating of the given score

        https://arcaea.fandom.com/wiki/Potential#Play_Rating

        :param constant: The (constant * 10) of the played chart, e.g. 120 for Testify[BYD]
        :param score: The score of the play result, e.g. 10002221
        :return: The play rating of the given values, e.g. Decimal("14.0")
        """
        if not isinstance(score, int):
            raise TypeError("score must be an integer")
        if not isinstance(constant, int):
            raise TypeError("constant must be an integer")
        if score < 0:
            raise ValueError("score cannot be negative")
        if constant < 0:
            raise ValueError("constant cannot be negative")

        score_modifier = cls.score_modifier(score)
        return max(Decimal(0), Decimal(constant) / 10 + score_modifier)

    class ConstantsFromPlayRatingResult(TypedDict):
        EX_PLUS: Tuple[Decimal, Decimal]
        EX: Tuple[Decimal, Decimal]
        AA: Tuple[Decimal, Decimal]
        A: Tuple[Decimal, Decimal]
        B: Tuple[Decimal, Decimal]
        C: Tuple[Decimal, Decimal]

    @classmethod
    def constants_from_play_rating(
        cls, play_rating: Union[Decimal, str, float, int]
    ) -> ConstantsFromPlayRatingResult:
        play_rating = Decimal(play_rating)

        def _result(score_upper: int, score_lower: int) -> Tuple[Decimal, Decimal]:
            upper_score_modifier = cls.score_modifier(score_upper)
            lower_score_modifier = cls.score_modifier(score_lower)
            return (
                play_rating - upper_score_modifier,
                play_rating - lower_score_modifier,
            )

        return {
            "EX_PLUS": _result(10000000, ScoreLowerLimits.EX_PLUS),
            "EX": _result(ScoreLowerLimits.EX_PLUS - 1, ScoreLowerLimits.EX),
            "AA": _result(ScoreLowerLimits.EX - 1, ScoreLowerLimits.AA),
            "A": _result(ScoreLowerLimits.AA - 1, ScoreLowerLimits.A),
            "B": _result(ScoreLowerLimits.A - 1, ScoreLowerLimits.B),
            "C": _result(ScoreLowerLimits.B - 1, ScoreLowerLimits.C),
        }
