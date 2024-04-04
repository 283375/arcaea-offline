from decimal import Decimal
from typing import Literal

from ._common import StepBooster


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
