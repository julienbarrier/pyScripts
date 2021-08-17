"""
superlattice calculations
"""

from typing import Optional
from scipy.constants import h, e
from numpy import arccos
from warning import warn


class superlattice:
    """
    class to evaluate some parameters in a given superlattice
    defaults are assuming graphene-hBN superlattice, but can easily be changed
    to account for bilayer graphene.
    """
    def __init__(self, name: str,
                 bzf: Optional[float] = 0,
                 secdp: Optional[float] = 0,
                 ab: Optional[float] = 0):
        self.name = name
        self.BrownZakfield = bzf
        self.secondaryDiracpoint = secdp
        self.AharonovBohm = ab

    def unit_length(self) -> float:
        if self.BrownZakfield:
            A_sl = h/e/self.BrownZakfield
        elif self.secondaryDiracpoint:
            A_sl = 4/self.secondaryDiracpoint
        elif self.AharonovBohm:
            A_sl = A_sl = h/e/self.AharonovBohm
        else:
            warn("please provide a value for the calculation")

        lambda_sl = (A_sl * 2 / 3**.5)**.5
        return lambda_sl

    def angle(self, delta: Optional[float] = 1.8/100) -> float:
        """
        args:
            self
            delta: 1.8/100 for graphene-hBN superlattice, 0 for bilayer
            graphene
        """
        lambda_sl = self.unit_length
        a = .246e-9
        phi = arccos(1+(delta**2 * lambda_sl**2 - (1+delta)**2 * a**2) /
                     (2*lambda_sl**2*(1+delta))
                     )
        return phi
