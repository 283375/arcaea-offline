from decimal import Decimal
from typing import Literal, Optional, Union


class PlayResult:
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


AwakenedIlithPartnerBonus = PartnerBonus(step_bonus="6.0")
AwakenedEtoPartnerBonus = PartnerBonus(step_bonus="7.0")
AwakenedLunaPartnerBonus = PartnerBonus(step_bonus="7.0")


class AwakenedAyuPartnerBonus(PartnerBonus):
    def __init__(self, step_bonus: Union[Decimal, str, float, int]):
        super().__init__(step_bonus=step_bonus)


AmaneBelowExPartnerBonus = PartnerBonus(final_multiplier="0.5")


class MithraTerceraPartnerBonus(PartnerBonus):
    def __init__(self, step_bonus: int):
        super().__init__(step_bonus=step_bonus)


MayaPartnerBonus = PartnerBonus(final_multiplier="2.0")


class StepBooster:
    def final_value(self) -> Decimal:
        raise NotImplementedError()


class LegacyMapStepBooster(StepBooster):
    def __init__(
        self,
        stamina: Literal[2, 4, 6],
        fragments: Literal[100, 250, 500, None],
    ):
        self.stamina = stamina
        self.fragments = fragments

    @property
    def stamina(self):
        return self.__stamina

    @stamina.setter
    def stamina(self, value: Literal[2, 4, 6]):
        if value not in [2, 4, 6]:
            raise ValueError("stamina can only be one of [2, 4, 6]")
        self.__stamina = value

    @property
    def fragments(self):
        return self.__fragments

    @fragments.setter
    def fragments(self, value: Literal[100, 250, 500, None]):
        if value not in [100, 250, 500, None]:
            raise ValueError("fragments can only be one of [100, 250, 500, None]")
        self.__fragments = value

    def final_value(self) -> Decimal:
        stamina_multiplier = Decimal(self.stamina)
        fragments_multiplier = Decimal(1)
        if self.fragments == 100:
            fragments_multiplier = Decimal("1.1")
        elif self.fragments == 250:
            fragments_multiplier = Decimal("1.25")
        elif self.fragments == 500:
            fragments_multiplier = Decimal("1.5")
        return stamina_multiplier * fragments_multiplier


class MemoriesStepBooster(StepBooster):
    def final_value(self) -> Decimal:
        return Decimal("4.0")


def calculate_step_original(
    play_result: PlayResult,
    *,
    partner_bonus: Optional[PartnerBonus] = None,
    step_booster: Optional[StepBooster] = None,
) -> Decimal:
    ptt = play_result.play_rating
    step = play_result.partner_step
    if partner_bonus:
        partner_bonus_step = partner_bonus.step_bonus
        partner_bonus_multiplier = partner_bonus.final_multiplier
    else:
        partner_bonus_step = Decimal("0")
        partner_bonus_multiplier = Decimal("1.0")

    result = (Decimal("2.45") * ptt.sqrt() + Decimal("2.5")) * (step / 50)
    result += partner_bonus_step
    result *= partner_bonus_multiplier
    if step_booster:
        result *= step_booster.final_value()

    return result


def calculate_step(
    play_result: PlayResult,
    *,
    partner_bonus: Optional[PartnerBonus] = None,
    step_booster: Optional[StepBooster] = None,
) -> Decimal:
    result_original = calculate_step_original(
        play_result, partner_bonus=partner_bonus, step_booster=step_booster
    )

    return round(result_original, 1)


def calculate_play_rating_from_step(
    step: Union[Decimal, str, int, float],
    partner_step_value: Union[Decimal, str, int, float],
    *,
    partner_bonus: Optional[PartnerBonus] = None,
    step_booster: Optional[StepBooster] = None,
):
    step = Decimal(step)
    partner_step_value = Decimal(partner_step_value)

    # get original play result
    if partner_bonus and partner_bonus.final_multiplier:
        step /= partner_bonus.final_multiplier
    if step_booster:
        step /= step_booster.final_value()

    if partner_bonus and partner_bonus.step_bonus:
        step -= partner_bonus.step_bonus

    play_rating_sqrt = (Decimal(50) * step - Decimal("2.5") * partner_step_value) / (
        Decimal("2.45") * partner_step_value
    )
    return play_rating_sqrt**2 if play_rating_sqrt >= 0 else -(play_rating_sqrt**2)
