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


class Gates:
    def __init__(self,
                n, D, Ctg:float, Cbg:float):
        self.n = n
        self.D = D
        self.ctg = Ctg
        self.cbg = Cbg

    def top_gate(self):
        return (e*self.n + 2*epsilon_0*self.D)/2/self.ctg

    def back_gate(self):
        return(e*self.n - 2*epsilon_0*self.D)/2/self.cbg

    def equation(self):
        coef = self.ctg/self.cbg
        intercept = self.back_gate()[0] - self.top_gate()[0] * coef
        print(f'V_b = {round(coef,3)} * V_t + {round(intercept,3)}')
        return coef, intercept

    def equation_tg(self):
        coef = self.cbg/self.ctg
        intercept = self.top_gate()[0] - self.back_gate()[0] * coef
        print(f'V_b = {round(coef,3)} * V_t + {round(intercept,3)}')
        return coef, intercept
