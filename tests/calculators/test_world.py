from decimal import ROUND_FLOOR, Decimal

from arcaea_offline.calculators.play_result import PlayResultCalculators
from arcaea_offline.calculators.world import (
    LegacyMapStepBooster,
    PartnerBonus,
    WorldMainMapCalculators,
    WorldPlayResult,
)


class TestWorldMainMapCalculators:
    def test_step_fandom(self):
        # Final result from https://arcaea.fandom.com/wiki/World_Mode_Mechanics#Calculation
        # CC BY-SA 3.0

        booster = LegacyMapStepBooster(6, 250)
        partner_bonus = PartnerBonus(step_bonus="+3.6")
        play_result = WorldPlayResult(play_rating=Decimal("11.299"), partner_step=92)
        result = WorldMainMapCalculators.step(
            play_result, partner_bonus=partner_bonus, step_booster=booster
        )

        assert result.quantize(Decimal("0.000")) == Decimal("175.149")

    def test_step(self):
        # Results from actual play results, Arcaea v5.5.8c

        def _quantize(decimal: Decimal) -> Decimal:
            return decimal.quantize(Decimal("0.0"), rounding=ROUND_FLOOR)

        # goldenslaughter FTR [9.7], 9906968
        # 10.7 > 34.2 < 160
        assert _quantize(
            WorldMainMapCalculators.step(
                WorldPlayResult(
                    play_rating=PlayResultCalculators.play_rating(9906968, 97),
                    partner_step=160,
                )
            )
        ) == Decimal("34.2")

        # Luna Rossa FTR [9.7], 9984569
        # 10.8 > 34.7 < 160
        assert _quantize(
            WorldMainMapCalculators.step(
                WorldPlayResult(
                    play_rating=PlayResultCalculators.play_rating(9984569, 97),
                    partner_step=160,
                )
            )
        ) == Decimal("34.7")

        # ultradiaxon-N3 FTR [10.5], 9349575
        # 10.2 > 32.7 < 160
        assert _quantize(
            WorldMainMapCalculators.step(
                WorldPlayResult(
                    play_rating=PlayResultCalculators.play_rating(9349575, 105),
                    partner_step=160,
                )
            )
        ) == Decimal("32.7")

        # san skia FTR [8.3], 10001036
        # 10.3 > 64.2 < 310
        assert _quantize(
            WorldMainMapCalculators.step(
                WorldPlayResult(
                    play_rating=PlayResultCalculators.play_rating(10001036, 83),
                    partner_step=310,
                )
            )
        ) == Decimal("64.2")
