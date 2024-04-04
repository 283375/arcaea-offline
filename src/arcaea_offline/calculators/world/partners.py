from ._common import PartnerBonus

AwakenedIlithPartnerBonus = PartnerBonus(step_bonus="6.0")
AwakenedEtoPartnerBonus = PartnerBonus(step_bonus="7.0")
AwakenedLunaPartnerBonus = PartnerBonus(step_bonus="7.0")


AmaneBelowExPartnerBonus = PartnerBonus(final_multiplier="0.5")


class MithraTerceraPartnerBonus(PartnerBonus):
    def __init__(self, step_bonus: int):
        super().__init__(step_bonus=step_bonus)


MayaPartnerBonus = PartnerBonus(final_multiplier="2.0")
