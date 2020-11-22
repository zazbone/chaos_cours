import numpy as np

from chaos import runge_kutta as rk

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


G = 1
D = 3


def ratio(ra, rb):
    return (rb - ra) / abs(rb - ra) ** 3


def dp_b1(t, r, m1, m2, m3):
    return G * m1 * (m2 * ratio(r[0], r[1]) + m3 * ratio(r[0], r[2]))

def dp_b2(t, r, m1, m2, m3):
    return G * m2 * (m1 * ratio(r[1], r[0]) + m3 * ratio(r[1], r[2]))

def dp_b3(t, r, m1, m2, m3):
    return G * m3 * (m1 * ratio(r[2], r[0]) + m2 * ratio(r[2], r[1]))

def dr_b1(t, p, m1, m2, m3):
    return p / m1

def dr_b2(t, p, m1, m2, m3):
    return p / m2

def dr_b3(t, p, m1, m2, m3):
    return p / m3


def main():
    m1, m2, m3 = 1, 1, 1
    r = np.random.uniform(-2, 2, size=(3, D))
    p = np.random.uniform(-0.2, 0.2, size=(3, D))

    sample = 1024
    t0 = 0
    dt = 0.01
    t = t0

    R1 = np.zeros(shape=(3, sample))
    R2 = np.zeros(shape=(3, sample))
    R3 = np.zeros(shape=(3, sample))

    for i in range(sample):
        p += rk.integr(t0=t, dt=dt, CI=r, func=(dp_b1, dp_b2, dp_b3), m1=m1, m2=m2, m3=m3)
        r += rk.integr(t0=t, dt=dt, CI=p, func=(dr_b1, dr_b2, dr_b3), m1=m1, m2=m2, m3=m3)
        R1[i] = r[0]
        R2[i] = r[1]
        R3[i] = r[2]

    ax = plt.axes(projection="3d")
    ax.plot3D(xs=R1, ys=R2, zs=R3, color="blue")
    plt.show()
