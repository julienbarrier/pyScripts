"""
functions to calculate 2DEG carrier density, Hall mobility and FET mobility
"""

from scipy.constants import e, epsilon_0
from typing import Optional


def density(
    dRxy: float,
    dB: float
) -> float:
    return dB / e / dRxy


def hall_mobility(
    dRxy: float,
    dB: float,
    Rxx: float,
    length: Optional[float] = 1,
    width: Optional[float] = 1
) -> float:

    return dRxy / dB / Rxx * length / width


def fet_mobility(
    dV_gate: float,
    d1_R: float,
    k: Optional[float] = 3.9,
    d: Optional[float] = 290e-9,
    length: Optional[float] = 1,
    width: Optional[float] = 1,
) -> float:

    Ci = k*epsilon_0/d
    return(d1_R / dV_gate * length / width / Ci)
