from numpy import logical_and, pi, sin
from lmfit.models import LinearModel, VoigtModel


def twotheta2q(
    twotheta,
    wavelength=0.154,
):
    ''''q as same unit as wavelength (reciprocal)'''
    return 4*pi/wavelength*sin(twotheta/2)


def fit_voigt_over_linear(
    q, I,
    cen=1,
    sig=0.002,
    sigmin=1e-4, sigmax=0.01,
    amplmin=0, amplmax=500,
    trim=0.06,
    plot=False
):

    trim = logical_and(q < cen + trim, q > cen - trim)
    q = q[trim]
    I = I[trim]

    mod = LinearModel()
    mod.set_param_hint('slope', value=-20)
    mod.set_param_hint('intercept', value=10)
    lineout = mod.fit(I, x=q)
    pars = lineout.params

    mod += VoigtModel()
    pars.add('center', value=cen)
    pars.add('sigma', value=sig, max=sigmax, min=sigmin)
    pars.add('amplitude', value=amplmin/2+amplmax/2, min=amplmin, max=amplmax)
    out = mod.fit(I, pars, x=q)

    return out
