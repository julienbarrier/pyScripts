"""
functions to trim a set of data
@julienbarrier
"""
import numpy as np
from warnings import warn


def trim_from_centre(x, y, centre, width):
    """
    trims x and y between values centre-width and centre+width of x
    """
    if len(x)-len(y) != 0:
        warn('x and y should be the same length')
    a = [None]*len(x)
    for i in range(len(x)):
        a[i] = [x[i], y[i]]
    filtered = filter(lambda val: abs(val[0]-centre) < width, a)
    f = np.array(list(filtered))
    return f[:, 0], f[:, 1]
