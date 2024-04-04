from decimal import Decimal
from typing import Optional, Union

from ._common import PartnerBonus, StepBooster, WorldPlayResult


class WorldMainMapCalculators:
    @staticmethod
    def step(
        play_result: WorldPlayResult,
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

    @staticmethod
    def play_rating_from_step(
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

        play_rating_sqrt = (
            Decimal(50) * step - Decimal("2.5") * partner_step_value
        ) / (Decimal("2.45") * partner_step_value)
        return (
            play_rating_sqrt**2 if play_rating_sqrt >= 0 else -(play_rating_sqrt**2)
        )
