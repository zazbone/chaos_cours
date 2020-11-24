import numpy as np
from numpy.linalg import norm

from chaos import runge_kutta as rk

import csv


G = 1
D = 3


class Body:
    def __init__(self, r, v, m):
        if np.shape(r) != np.shape(v):
            raise ValueError("Speed and position vector must have same dimension")
        self.r = np.array(r)
        self.v = np.array(v)
        self.m = m


class ThreeBody():
    G = 6.7e-11

    def __init__(self, r1, r2, r3, v1, v2, v3, m1, m2, m3):
        self.r = np.array([r1, r2, r3])
        self.v = np.array([v1, v2, v3])
        self.m = np.array([m1, m2, m3])

    @classmethod
    def from_body(cls, body1: Body, body2: Body, body3: Body):
        return cls(
            r1=body1.r, r2=body2.r, r3=body3.r,
            v1=body1.v, v2=body2.v, v3=body3.v,
            m1=body1.m, m2=body2.m, m3=body3.m,
        )

    def p(self):
        return np.array([
            [self.m[0], 0, 0],
            [0, self.m[1], 0],
            [0, 0, self.m[0]],
        ]) * self.v

    @classmethod
    def a(cls):
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


def write_data(writer, fieldnames, gen, time, r, v):
    row = {"gen": gen, "time": time}
    for i in range(1, 4):
        row[f"x{i}"] = r[i - 1][0]
        row[f"y{i}"] = r[i - 1][1]
        row[f"z{i}"] = r[i - 1][2]
        row[f"v_x{i}"] = v[i - 1][0]
        row[f"v_y{i}"] = v[i - 1][1]
        row[f"v_z{i}"] = v[i - 1][2]
    writer.writerow(row)


def solar_sys():
    # Initial orbital parameters
    MOON = Body(
        [1.5038e11, 0, 0],
        [0, 4e4, 0],
        7e22
    )
    EARTH = Body(
        [1.5e11, 0, 0],
        [0, 3e4, 0],
        6e24
    )
    SUN = Body(
        [0, 0, 0],
        [0, 0, 0],
        2e30
    )

    system = ThreeBody.from_body(MOON, EARTH, SUN)

    t0 = 0
    t = t0
    sample = 0b1 << 15
    dt = (4 * 30.5 * 24 * 3600) / 1024  # 4 mois d'étude

    with open("result.csv", "w") as csv_file:
        fields_names = ["gen", "time"]
        for i in range(1, 4):
            fields_names.extend((f"Body{i}", f"x{i}", f"y{i}", f"z{i}", f"v_x{i}", f"v_y{i}", f"v_z{i}"))
        writer = csv.DictWriter(csv_file, fieldnames=fields_names)
        writer.writeheader()
        for i in range(sample):
            write_data(writer, fields_names, i, t, system.r, system.v)
            system.v += rk.integr(t0=t, dt=dt, CI=system.r, func=ThreeBody.a(), m1=system.m[0], m2=system.m[1], m3=system.m[2])
            system.r += rk.integr(t0=t, dt=dt, CI=system.v, func=ThreeBody.dr())
            t += dt
