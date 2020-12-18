def rk(t0: float, dt: float, CI, func, *args):
    k1 = func(t0, CI, *args)
    k2 = func(t0 + dt / 2, CI + dt * k1 / 2, *args)
    k3 = func(t0 + dt / 2, CI + dt * k2 / 2, *args)
    k4 = func(t0 + dt, CI + dt * k3, *args)
    return (1/6) * (k1 + 2*k2 + 2*k3 + k4) * dt