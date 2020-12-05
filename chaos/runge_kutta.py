def integr(t0: float, dt: float, CI, func, **kwargs):
    """\
    4rd ordre Runge-kutta algorithm implémentation one or more (numpy array) variable
    Compute only one step
    t0: init_time
        (must be an argument of your integration function, \
    event if time does not interfer in the system)
    dt: time interval of the numerical integration
    CI: List of the initial condition values
    func: function to integrate, \
        f(t, CI, kwargs)
    **kwargs: all possible fuctions extra arguments constant \
    (name all your arguments to avoid conflicts)
    return: result of integration, one or more (numpy array) variable
    See lorentz.py for an example with lorentz attractor system\
    """
    k1 = func(t0, CI, **kwargs)
    k2 = func(t0 + dt / 2, CI + dt * k1 / 2, **kwargs)
    k3 = func(t0 + dt / 2, CI + dt * k2 / 2, **kwargs)
    k4 = func(t0 + dt, CI + dt * k3 / 2, **kwargs)
    return (1/6) * (k1 + 2*k2 + 2*k3 + k4) * dt
