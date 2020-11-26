import numpy as np
from numpy.linalg import norm

from chaos import runge_kutta as rk
from chaos._config import Config

import csv


G = 1
D = 3


class Body:
    G = 1
    def __init__(self, r, v, m):
        if np.shape(r) != np.shape(v):
            raise ValueError("Speed and position vector must have same dimension")
        self.r = np.array(r)
        self.v = np.array(v)
        self.m = m


class ThreeBody():
    def __init__(self, r1, r2, r3, v1, v2, v3, m1, m2, m3):
        self.r = np.array([r1, r2, r3])
        self.v = np.array([v1, v2, v3])
        self.m = np.array([m1, m2, m3])
        self.G = G


    @classmethod
    def from_config(cls, config: Config):
        cls.G = config.G
        return cls(
            r1=config.b_pos[0], r2=config.b_pos[1], r3=config.b_pos[2],
            v1=config.b_speed[0], v2=config.b_speed[1], v3=config.b_speed[2],
            m1=config.b_mass[0], m2=config.b_mass[1], m3=config.b_mass[2],
        )

    def p(self):
        return np.array([
            [self.m[0], 0, 0],
            [0, self.m[1], 0],
            [0, 0, self.m[2]],
        ]) * self.v

    @classmethod
    def dv(cls):
        return cls.a1, cls.a2, cls.a3

    @classmethod
    def a1(cls, t, r, m1, m2, m3):
        return cls.G * (m2 * ratio(r[0], r[1]) + m3 * ratio(r[0], r[2]))

    @classmethod
    def a2(cls, t, r, m1, m2, m3):
        return cls.G * (m1 * ratio(r[1], r[0]) + m3 * ratio(r[1], r[2]))

    @classmethod
    def a3(cls, t, r, m1, m2, m3):
        return cls.G * (m1 * ratio(r[2], r[0]) + m2 * ratio(r[2], r[1]))

    @classmethod
    def dr(cls):
        return cls.dr1, cls.dr2, cls.dr3

    @staticmethod
    def dr1(t, v):
        return v[0]

    @staticmethod
    def dr2(t, v):
        return v[1]

    @staticmethod
    def dr3(t, v):
        return v[2]


def ratio(ra, rb):
    return (rb - ra) / norm(rb - ra) ** 3


def write_data(writer, config, system, i, t, acc):
    row = {"gen": i, "time": t}
    for i in range(3):
        if config.get_pos:
            row[f"x_{i+1}"] = system.r[i][0]
            row[f"y_{i+1}"] = system.r[i][1]
            row[f"z_{i+1}"] = system.r[i][2]
        if config.get_speed:
            row[f"vx_{i+1}"] = system.v[i][0]
            row[f"vy_{i+1}"] = system.v[i][1]
            row[f"vz_{i+1}"] = system.v[i][2]
        if config.get_acc:
            row[f"ax_{i+1}"] = acc[i][0]
            row[f"ay_{i+1}"] = acc[i][1]
            row[f"az_{i+1}"] = acc[i][2]
    writer.writerow(row)


def tb_main(config_path="out.json"):
    config = Config(config_path)
    system = ThreeBody.from_config(config)

    t0 = 0
    t = t0
    sample = config.sample
    dt = config.tf / sample  # 4 mois d'étude

    with open("result.csv", "w") as csv_file:
        fields_names = _create_fields(config)
        writer = csv.DictWriter(csv_file, fieldnames=fields_names)
        writer.writeheader()

        for i in range(sample):
            if not i % config.keeped_sample:
                delta_v = rk.integr(t0=t, dt=dt, CI=system.r, func=ThreeBody.dv(), m1=system.m[0], m2=system.m[1], m3=system.m[2])
                write_data(writer, config, system, i, t, delta_v)
            system.v = system.v + delta_v
            system.r = system.r + rk.integr(t0=t, dt=dt, CI=system.v, func=ThreeBody.dr())
            t += dt


def _create_fields(config: Config):
    fields_names = ["gen", "time"]
    for i in range(3):
        fields_names.extend([config.b_name[i]])
        if config.get_pos:
            fields_names.extend([f"x_{i+1}", f"y_{i+1}", f"z_{i+1}"])
        if config.get_speed:
            fields_names.extend([f"vx_{i+1}", f"vy_{i+1}", f"vz_{i+1}"])
        if config.get_acc:
            fields_names.extend([f"ax_{i+1}", f"ay_{i+1}", f"az_{i+1}"])
    return fields_names