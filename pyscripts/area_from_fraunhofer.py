"""
area from fraunhofer
calculate characteristic area from a fraunhofer-shaped field-dependent
critical current in a superconductor
"""

from scipy.constants import h, e
from warning import warn
from typing import Optional
from numpy import deg2rad, sin


def area(deltaB: float, unit: str = 'm') -> float:
    A = h/e/deltaB
    if unit == 'm' or unit == 'meter':
        area = A
    elif unit == 'cm' or unit == 'centimeter':
        area = A*10**4
    elif unit == 'um' or unit == 'µm' or unit == 'micrometer':
        area = A*10**12
    elif unit == 'nm' or unit == 'nanometer':
        area = A*10**18
    else:
        warn('chose a proper unit: m, cm, um or nm')
        area = 0
    return area


def deltaB(A: float) -> float:
    return h/e/A


def triangular_area(unit_length: float) -> float:
    return 3**.5/4 * unit_length**2


def triangle_domain(area: float) -> float:
    return (area * 4 / 3**.5)**.5


def unit_length(rad: Optional[float] = None,
                deg: Optional[float] = None) -> float:
    if rad and deg and rad != deg2rad(deg):
        warn("you gave two inconsistent values")
    elif not rad and not deg:
        warn("please give a value")
    elif deg:
        rad = deg2rad(deg)

    a = 0.246e-9  # graphene's lattice constant
    return a/2/sin(rad/2)
