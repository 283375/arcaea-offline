from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreLowerLimits:
    EX_PLUS = 9900000
    EX = 9800000
    AA = 9500000
    A = 9200000
    B = 8900000
    C = 8600000
    D = 0
