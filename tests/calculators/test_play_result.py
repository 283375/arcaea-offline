from decimal import Decimal

import pytest

from arcaea_offline.calculators.play_result import PlayResultCalculators


class TestPlayResultCalculators:
    def test_score_modifier(self):
        # Results from https://arcaea.fandom.com/wiki/Potential#Score_Modifier

        assert PlayResultCalculators.score_modifier(10000000) == Decimal("2.0")
        assert PlayResultCalculators.score_modifier(9900000) == Decimal("1.5")
        assert PlayResultCalculators.score_modifier(9800000) == Decimal("1.0")
        assert PlayResultCalculators.score_modifier(9500000) == Decimal("0.0")
        assert PlayResultCalculators.score_modifier(9200000) == Decimal("-1.0")
        assert PlayResultCalculators.score_modifier(8900000) == Decimal("-2.0")
        assert PlayResultCalculators.score_modifier(8600000) == Decimal("-3.0")

        assert PlayResultCalculators.score_modifier(0).quantize(
            Decimal("-0.00")
        ) == Decimal("-31.67")

        pytest.raises(ValueError, PlayResultCalculators.score_modifier, -1)

        pytest.raises(TypeError, PlayResultCalculators.score_modifier, "9800000")
        pytest.raises(TypeError, PlayResultCalculators.score_modifier, None)
        pytest.raises(TypeError, PlayResultCalculators.score_modifier, [])

    def test_play_rating(self):
        assert PlayResultCalculators.play_rating(10002221, 120) == Decimal("14.0")

        assert PlayResultCalculators.play_rating(5500000, 120) == Decimal("0.0")

        pytest.raises(TypeError, PlayResultCalculators.play_rating, "10002221", 120)
        pytest.raises(TypeError, PlayResultCalculators.play_rating, 10002221, "120")
        pytest.raises(TypeError, PlayResultCalculators.play_rating, "10002221", "120")

        pytest.raises(TypeError, PlayResultCalculators.play_rating, 10002221, None)

        pytest.raises(ValueError, PlayResultCalculators.play_rating, -1, 120)
        pytest.raises(ValueError, PlayResultCalculators.play_rating, 10002221, -1)
