## fit_neutron_scattering.py
## Julien Barrier
## @julienbarrier
##
## Fit peaks from Neutron Scattering data, with a Gaussian (Elastic) +
## Laurentzian (QES) functions
## We use our own model definitions otherwise lmfit overwrites the parameters.

from lmfit import Model

def linear(x,sl,inter):
    return sl*x + inter

def gaussian(x,cen,fwhm,Gampl):
    sig = fwhm / (2*np.sqrt(2 * np.log(2)))
    return Gampl * np.exp(-(x-cen)**2 / (2*sig**2)) / (sig * np.sqrt(2*np.pi))

def lorentzian(x,cen,gamma,Lampl):
    return Lampl / (np.pi*gamma) * (1/ (((x-cen)/gamma)**2 + 1))

def linear_gaussian_lorentzian(x,cen=0,slope=0,intercept=0,fwhm=.27,gamma=.3,Gampl=10,Lampl=10):
    return linear(x,slope,intercept) + gaussian(x,cen,fwhm,Gampl) + lorentzian(x,cen,gamma,Lampl)

def gaussian_lorentzian(x,cen=0,offset=0,fwhm=.27,gamma=.3,Gampl=10,Lampl=10):
    return offset + gaussian(x,cen,fwhm,Gampl) + lorentzian(x,cen,gamma,Lampl)

def fit_gaussian_lorentzian(ET, I, cen=0, offset=10, fwhm = .27, gamma = .3, Gampl=10, Lampl=10, fixcen=False,fixline=False,plot=False):

    mod = Model(gaussian_lorentzian)
    mod.set_param_hint('fwhm', value = fwhm, vary = False)
    mod.set_param_hint('cen', value = cen, vary = not fixcen)
    mod.set_param_hint('offset',value=offset, vary = not fixline)

    out = mod.fit(I, x=ET,offset=offset,gamma=gamma,Gampl=Gampl,Lampl=Lampl)

    if plot:
        fig = plt.figure()
        out.plot_fit()

    return out
