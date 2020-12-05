import numpy as np
from numpy.linalg import norm

from chaos import runge_kutta as rk
from chaos._config import Config
from chaos.data_proc import init_frame, write_data, plot_frame


class ThreeBody():
    def __init__(self, r1, r2, r3, v1, v2, v3, m1, m2, m3):
        self.r = np.array([r1, r2, r3])
        self.v = np.array([v1, v2, v3])
        self.m = np.array([m1, m2, m3])

    def __str__(self):
        return "\n".join((str(i) for i in self.r))

    @classmethod
    def from_config(cls, config: Config):
        cls.G = config.G
        return cls(
            r1=config.b_pos[0], r2=config.b_pos[1], r3=config.b_pos[2],
            v1=config.b_speed[0], v2=config.b_speed[1], v3=config.b_speed[2],
            m1=config.b_mass[0], m2=config.b_mass[1], m3=config.b_mass[2],
        )


def dv(t, r, m, G):
    a1 = G * (m[1] * ratio(r[0], r[1]) + m[2] * ratio(r[0], r[2]))
    a2 = G * (m[0] * ratio(r[1], r[0]) + m[2] * ratio(r[1], r[2]))
    a3 = G * (m[0] * ratio(r[2], r[0]) + m[1] * ratio(r[2], r[1]))
    return np.array([a1, a2, a3])


def dr(t, v):
    return v


def ratio(ra, rb):
    return (rb - ra) / norm(rb - ra) ** 3


def tb_main(config_path="out.json"):
    config = Config(config_path)
    system = ThreeBody.from_config(config)

    t0 = 0
    t = t0
    dt = config.dt()

    data_frame = init_frame(config)

    for i in range(config.sample):
        delta_v = rk.integr(t0=t, dt=dt, CI=system.r, func=dv, m=system.m, G=config.G)
        if not i % config.keeped_sample:
            write_data(data_frame, config, system, i, t, delta_v)
        system.v = system.v + delta_v  # Numpy error with in place add
        system.r = system.r + rk.integr(t0=t, dt=dt, CI=system.v, func=dr)
        t += dt

    data_frame.to_csv(config_path.with_suffix(".csv"))
    plot_frame(data_frame, config, ["x_2", "y_2"])
