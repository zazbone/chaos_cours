import numpy as np


def integr(t0: float, dt: float, CI: np.ndarray, func: tuple, **kwargs) -> np.ndarray:
    """\
    4rd ordre Runge-kutta algorithm implémentation for n variables
    Compute only one step

    t0: init_time
        (must be an argument of your integration function, event if time does not interfer in the system)
    dt: time interval of the numerical integration
    CI: List of the initial condition values
    func: function array that contains all function to integrate, can be any sequence of callable objects
    **kwargs: all possible fuctions extra arguments constant (name all your arguments to avoid conflicts)

    return: numpy ndarray of shape=n where n is the numbre of init conditions
        Contains CI integral

    See lorentz.py for an example with lorentz attractor system\
    """

    shape_ci = np.shape(CI)
    len_ci = shape_ci[0]
    if len_ci != len(func):
        raise ValueError("func array must have the same size as CI array")

    k = np.zeros(shape=(4, *shape_ci))

    # k1
    for i, fn in enumerate(func):
        k[0][i] = fn(t0, CI, **kwargs)
    # k2
    for i, fn in enumerate(func):
        k[1][i] = fn(t0 + dt / 2, CI + dt * k[0] / 2, **kwargs)
    # k3
    for i, fn in enumerate(func):
        k[2][i] = fn(t0 + dt / 2, CI + dt * k[1] / 2, **kwargs)
    # k4
    for i, fn in enumerate(func):
        k[3][i] = fn(t0 + dt, CI + dt * k[2], **kwargs)

    h = np.zeros(shape=shape_ci)
    for i in range(len_ci):
        h[i] = (1/6) * (k[0][i] + 2*k[1][i] + 2*k[2][i] + k[3][i]) * dt
    return h
