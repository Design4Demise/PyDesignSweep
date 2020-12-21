import numpy as np
from scipy import interpolate


def check_spar(filename: str, chord_length: float, h: float, b: float, htol: float, btol: float) -> bool:

    """Checks if spar fits in aerofoil geometry.

    Parameters
    ----------
    filename: str
        Filename to aerofoil geometry coordinates.

    chord_length: float
        Chord length.

    h: float
        Height of spar.

    b: float
        Width of spar.

    htol: float
        Tolerance for the height either side.

    btol: float
        Tolerance for the width either side.
    

    Returns
    -------
    bool
        True if spar fits, False otherwise
    """

    try:
        af = np.loadtxt(filename, skiprows=1, delimiter=',')
    except ValueError:
        raise ValueError('Please ensure appropriate file format.')

    # scale aerofoil
    af *= chord_length

    # add tolerances
    b += 2 * btol
    h += 2 * htol

    # split aerofoil into upper/lower surfaces
    arr_upper, arr_lower = np.split(af, [np.argmin(af[:, 0])])
    arr_upper = np.flipud(arr_upper)

    if b > chord_length or h > (np.max(np.abs(arr_upper[:, 1] - arr_lower[1:, 1]))):
        return False

    # provide linear interpolations
    od_interp_upper = interpolate.interp1d(arr_upper[:, 0], arr_upper[:, 1])
    od_interp_lower = interpolate.interp1d(arr_lower[:, 0], arr_lower[:, 1])

    max_b = np.max(arr_upper[:, 1])
    min_b = np.min(arr_lower[:, 1])

    loc_max_h = np.argmax(np.abs(arr_upper[:, 1] - arr_lower[1:, 1]))

    x_hmax = arr_upper[loc_max_h][0]
    yc_hmax = 0.5 * (arr_upper[loc_max_h][1] + arr_lower[loc_max_h][1])

    # calculate bounds
    lb_b, ub_b = [x_hmax + i * b / 2 for i in [-1, 1]]
    lb_h, ub_h = [yc_hmax + i * h / 2 for i in [-1, 1]]

    for h_bound in [ub_h, lb_h]:
        for b_bound in [ub_b, lb_b]:
            if not h_bound < od_interp_upper(b_bound) and h_bound > od_interp_lower(b_bound):
                return False

    return True
