import chaos.runge_kutta as rk

import numpy as np

import matplotlib.pyplot as plt

from pathlib import Path


# Time does not interfer
def dxyz(t, point: np.ndarray, sigma, rho, beta):
    dx = sigma * (point[1] - point[0])
    dy = rho * point[0] - point[1] - point[0] * point[2]
    dz = point[0] * point[1] - beta * point[2]
    return np.array([dx, dy, dz])


def lorentz():
    sample = 5000

    rho = 28
    sigma = 10
    beta = 8 / 3

    point = np.array([0, 0.1, 0])

    TRAJECTORY = np.zeros(shape=(3, sample))

    t0 = 0
    dt = 0.01

    for i in range(sample):
        point = point + rk.integr(t0=t0, dt=dt, CI=point, func=dxyz, rho=rho, sigma=sigma, beta=beta)
        TRAJECTORY[..., i] = point

    ax = plt.axes(projection="3d")
    ax.plot3D(xs=TRAJECTORY[0], ys=TRAJECTORY[1], zs=TRAJECTORY[2], color="blue")
    path = Path(__file__).parent / "Lorentz" / "fig.png"
    plt.savefig(path)
    plt.show()


lorentz()
