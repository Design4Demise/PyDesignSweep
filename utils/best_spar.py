from .check_spar import check_spar


def best_spar(aerofoil, chord_length, h_range, b_range, h_tol, b_tol):
    best_iy = 0
    best_h = None
    best_b = None

    for h in h_range:
        for b in b_range:
            iy = b * h ** 3 / 12
            if check_spar(aerofoil, chord_length, h, b, h_tol, b_tol) and iy > best_iy:
                best_iy = iy
                best_h = h
                best_b = b

    return best_h, best_b
