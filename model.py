"""Carbon-aware EOQ model from Hua, Cheng & Wang (2010), equations 5-7.

Notation:
    K       fixed ordering cost per order
    h       annual holding cost per unit
    e       carbon emissions per order (variable transport coefficient)
    g       carbon emissions per unit held (variable warehouse coefficient)
    D       annual demand
    C       carbon price per unit
    alpha   carbon emission cap per unit time
"""

import numpy as np


def Q_eoq(K, h, D):
    """Classical EOQ Q^0 = sqrt(2KD/h)."""
    return np.sqrt(2 * K * D / h)


def Q_hat(e, g, D):
    """Carbon-minimizing Q_hat = sqrt(2eD/g)."""
    return np.sqrt(2 * e * D / g)


def Q_star(K, h, e, g, C, D):
    """Optimal Q* under cap-and-trade (eq. 6): sqrt(2(K+Ce)D/(h+Cg))."""
    return np.sqrt(2 * (K + C * e) * D / (h + C * g))


def TC_eoq(K, h, D):
    """Classical EOQ cost TC_0 = sqrt(2KDh)."""
    return np.sqrt(2 * K * D * h)


def TC_star(K, h, e, g, C, alpha, D):
    """Total cost at Q* (eq. 7): sqrt(2D(K+Ce)(h+Cg)) - C*alpha."""
    return np.sqrt(2 * D * (K + C * e) * (h + C * g)) - C * alpha


def alpha_threshold(K, h, e, g, C, D):
    """Buy/sell threshold alpha_0 from Theorem 3."""
    a = e * np.sqrt((h + C * g) * D / (2 * (K + C * e)))
    b = g * np.sqrt((K + C * e) * D / (2 * (h + C * g)))
    return a + b


def carbon_footprint(Q, e, g, D):
    """CF(Q) = eD/Q + gQ/2."""
    return e * D / Q + g * Q / 2


def transfer(K, h, e, g, C, alpha, D):
    """X = alpha - CF(Q*); positive = sell credit, negative = buy."""
    Q = Q_star(K, h, e, g, C, D)
    return alpha - carbon_footprint(Q, e, g, D)


def delta_CO2(K, h, e, g, C, D):
    """Carbon savings vs EOQ: CF(Q^0) - CF(Q*)."""
    Q0 = Q_eoq(K, h, D)
    Qs = Q_star(K, h, e, g, C, D)
    return carbon_footprint(Q0, e, g, D) - carbon_footprint(Qs, e, g, D)


def delta_TC(K, h, e, g, C, alpha, D):
    """Cost change vs EOQ: TC(Q*) - TC_0."""
    return TC_star(K, h, e, g, C, alpha, D) - TC_eoq(K, h, D)
