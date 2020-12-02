import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from csv import DictReader


def plot_2D(x, y):
    plt.plot(x, y, marker='.', linestyle='None', markersize=0.1)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


def from_double_gen(generator, *args):
    x_array = []
    y_array = []
    for x, y in generator(*args):
        x_array.append(x)
        y_array.append(y)
    x_array = np.array(x_array)
    y_array = np.array(y_array)
    plot_2D(x_array, y_array)


def plot_xy(path):
    with open(Path(path).with_suffix(".csv"), "r") as csv_file:
        reader = DictReader(csv_file, fieldnames=["x_1", "y_1", "x_2", "y_2", "x_3", "y_3",])
        x1 = []
        x2 = []
        x3 = []
        y1 = []
        y2 = []
        y3 = []
        for row in reader:
            x1.append(row["x_1"])
            x2.append(row["x_2"])
            x3.append(row["x_3"])
            y1.append(row["y_1"])
            y2.append(row["y_2"])
            y3.append(row["y_3"])
        plt.plot(x1, y1)
        plt.plot(x2, y2)
        plt.plot(x3, y3)
        plt.savefig(Path(path).with_suffix(".png"))
