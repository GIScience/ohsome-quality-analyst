import numpy as np


def sigmoid(x: float, x_0: float, k: float, L: float):
    """Sigmoid function/curve.

    Args:
        L: the curve's maximum value / asymptotic (the plateaus);
        k: the logistic growth rate or steepness of the curve
        x_0: the x value of the sigmoid's midpoint (inflection point)
    """
    return L / (1 + np.exp(-k * (x - x_0)))


def sigmoid_1(x, x_0, k, L):
    return sigmoid(x, x_0, k, L)


# fmt: off
def sigmoid_2(x, x_01, x_02, k1, k2, L1, L2):
    """Sigmoid with 2 jumps."""
    _L2 = L2 - L1
    return (
        sigmoid(x, x_01, k1, L1)
        + sigmoid(x, x_02, k2, _L2)
    )


def sigmoid_3(x, x_01, x_02, x_03, k1, k2, k3, L1, L2, L3):
    """Sigmoid with 3 jumps."""
    _L3 = L3 - L2
    _L2 = L2 - L1
    return (
        sigmoid(x, x_01, k1, L1)
        + sigmoid(x, x_02, k2, _L2)
        + sigmoid(x, x_03, k3, _L3)
    )


def sigmoid_4(x, x_01, x_02, x_03, x_04, k1, k2, k3, k4, L1, L2, L3, L4):
    """Sigmoid with 3 jumps."""
    _L4 = L4 - L3
    _L3 = L3 - L2
    _L2 = L2 - L1
    return (
        sigmoid(x, x_01, k1, L1)
        + sigmoid(x, x_02, k2, _L2)
        + sigmoid(x, x_03, k3, _L3)
        + sigmoid(x, x_04, k4, _L4)
    )
# fmt: on
