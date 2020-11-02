import numpy as np
import matplotlib.pyplot as plt



def plot_2D(x, y):
    plt.plot(x, y, marker='.', linestyle = 'None', markersize=0.1)
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
