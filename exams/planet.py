import numpy as np
from numpy.linalg import norm
from json import load
import matplotlib.pyplot as plt
from integr import rk


class Planetoid:
    def __init__(self, ra, rb, ma, mb, G):
        ra = np.array(ra)
        rb = np.array(rb)
        # Center of mass
        self.C = (ma * ra + mb * rb) / (ma + mb)
        # We only need to keep trace of vector norm to definine there position each t
        self.ra = norm(ra)
        self.rb = norm(rb)
        # masses and G constant are always factorized in the equation
        self.mag = ma * G
        self.mbg = ma * G
        # Kepler 3rd law
        self.omega = np.sqrt((self.mag + self.mbg) / pow(norm(self.rb - self.ra), 3))

    def vec_ra(self, t):
        return -self.ra * rot_mat(self.omega * t)

    def vec_rb(self, t):
        return self.rb * rot_mat(self.omega * t)


def rot_mat(angle):
    return np.array([
        np.cos(angle),
        np.sin(angle)
    ])

def calc_acc(t, planet_pos, obj):
        MA = obj.vec_ra(t) - planet_pos
        MB = obj.vec_rb(t) - planet_pos
        return obj.mag * MA / np.power(norm(MA),3) + obj.mbg * MB / np.power(norm(MB),3)

def calc_spd(_t, v):
    return v

def main():
    plt.clf()
    with open("planet.json", "r") as js:
        config = load(js)
    planetoid = Planetoid(**config)

    r = np.array([0.4, -0.866])
    delta_v = 0
    t0 = 0
    dt = 0.01
    sample = int(4 / dt)

    R = np.zeros((sample, 3, 2))
    T = np.linspace(t0, t0 + dt * sample, sample)

    for i, t in enumerate(T):
        R[i] = np.array([r, planetoid.vec_ra(t), planetoid.vec_rb(t)])
        delta_v = delta_v + rk(t, dt, r, calc_acc, planetoid)
        r = r + rk(t, dt, delta_v, calc_spd)
    
    plt.plot(R[:, 0, 0], R[:, 0, 1], "r-")
    plt.plot(R[:, 1, 0], R[:, 1, 1], "b-")
    plt.plot(R[:, 2, 0], R[:, 2, 1], "b-")

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Planetoid mouvement")

    plt.savefig("planetoid.png")