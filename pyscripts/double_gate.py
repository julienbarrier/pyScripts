"""
calculate several parameters when working on double gated devices
"""

from scipy.constants import e, epsilon_0


class DoubleGate:
    """
    class to evaluate double gate parameters in a given device
    """
    def __init__(self,
                 Vtg,
                 Vbg,
                 Ctg: float,
                 Cbg: float
                 ):
        self.vtg = Vtg
        self.vbg = Vbg
        self.ctg = Ctg
        self.cbg = Cbg

    def density(self):
        return (self.ctg * self.vtg + self.cbg * self.vbg)/e

    def displacement(self):
        return (self.ctg * self.vtg - self.cbg * self.vbg)/2/epsilon_0
