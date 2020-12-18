import numpy as np
from numpy.linalg import norm
from integr import rk
from json import load
import matplotlib.pyplot as plt


class ThreeBody():
    def __init__(self, config):
        self.r = np.array(config["r"])
        self.v = np.array(config["v"])
        # Masses always in factor with G
        self.gm = np.array(config["m"]) * config["G"]


def dv(_t, r, gm):
    a1 = (gm[1] * ratio(r[0], r[1]) + gm[2] * ratio(r[0], r[2]))
    a2 = (gm[0] * ratio(r[1], r[0]) + gm[2] * ratio(r[1], r[2]))
    a3 = (gm[0] * ratio(r[2], r[0]) + gm[1] * ratio(r[2], r[1]))
    return np.array([a1, a2, a3])

def dr(_t, v):
    return v

def ratio(ra, rb):
    return (rb - ra) / norm(rb - ra) ** 3

def main(config):
    system = ThreeBody(config)
    dt = config["duration"] / config["samples"]
    T = np.linspace(0, config["duration"], config["samples"])

    R = np.zeros((config["samples"], 3, 2))

    for i, t in enumerate(T):
        R[i] = system.r
        system.v = system.v + rk(t, dt, system.r, dv, system.gm)
        system.r = system.r + rk(t, dt, system.v, dr)
    
    plt.plot(R[:, 0, 0], R[:, 0, 1], config["plot"]["format"][0])
    plt.plot(R[:, 1, 0], R[:, 1, 1], config["plot"]["format"][1])
    plt.plot(R[:, 2, 0], R[:, 2, 1], config["plot"]["format"][2])

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(config["plot"]["title"])

    plt.savefig(config["plot"]["png name"] + ".png")
