from decimal import Decimal

from arcaea_offline.calculate.world_step import (
    AwakenedAyuPartnerBonus,
    LegacyMapStepBooster,
    PlayResult,
    calculate_step_original,
)


def test_world_step():
    # the result was copied from https://arcaea.fandom.com/wiki/World_Mode_Mechanics#Calculation
    # CC BY-SA 3.0

    booster = LegacyMapStepBooster(6, 250)
    partner_bonus = AwakenedAyuPartnerBonus("+3.6")
    play_result = PlayResult(play_rating=Decimal("11.299"), partner_step=92)
    result = calculate_step_original(
        play_result, partner_bonus=partner_bonus, step_booster=booster
    )

    assert result.quantize(Decimal("0.000")) == Decimal("175.149")
