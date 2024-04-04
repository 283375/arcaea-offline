from decimal import Decimal
from typing import Union


class WorldPlayResult:
    def __init__(
        self,
        *,
        play_rating: Union[Decimal, str, float, int],
        partner_step: Union[Decimal, str, float, int],
    ):
        self.__play_rating = play_rating
        self.__partner_step = partner_step

    @property
    def play_rating(self):
        return Decimal(self.__play_rating)

    @property
    def partner_step(self):
        return Decimal(self.__partner_step)


class PartnerBonus:
    def __init__(
        self,
        *,
        step_bonus: Union[Decimal, str, float, int] = Decimal("0.0"),
        final_multiplier: Union[Decimal, str, float, int] = Decimal("1.0"),
    ):
        self.__step_bonus = step_bonus
        self.__final_multiplier = final_multiplier

    @property
    def step_bonus(self):
        return Decimal(self.__step_bonus)

    @property
    def final_multiplier(self):
        return Decimal(self.__final_multiplier)


class StepBooster:
    def final_value(self) -> Decimal:
        raise NotImplementedError()


class MemoriesStepBooster(StepBooster):
    def final_value(self) -> Decimal:
        return Decimal("4.0")
