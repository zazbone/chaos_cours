import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


def init_frame(config):
    zero = np.zeros(shape=config.sample // config.keeped_sample)
    fields = {
        "time": zero
    }
    for i in range(1, 4):
        if config.get_pos:
            fields[f"x_{i}"] = zero
            if config.dim > 1:
                fields[f"y_{i}"] = zero
            if config.dim > 2:
                fields[f"z_{i}"] = zero
        if config.get_speed:
            fields[f"vx_{i}"] = zero
            if config.dim > 1:
                fields[f"vy_{i}"] = zero
            if config.dim > 2:
                fields[f"vz_{i}"] = zero
        if config.get_acc:
            fields[f"ax_{i}"] = zero
            if config.dim > 1:
                fields[f"ay_{i}"] = zero
            if config.dim > 2:
                fields[f"az_{i}"] = zero

    return pd.DataFrame(fields)


def write_data(data_frame, config, system, sample, t, acc):
    data_frame["time"][sample] = t
    for i in range(3):
        if config.get_pos:
            data_frame[f"x_{i+1}"][sample] = system.r[i][0]
            if config.dim > 1:
                data_frame[f"y_{i+1}"][sample] = system.r[i][1]
            if config.dim > 2:
                data_frame[f"z_{i+1}"][sample] = system.r[i][2]
        if config.get_speed:
            data_frame[f"vx_{i+1}"][sample] = system.v[i][0]
            if config.dim > 1:
                data_frame[f"vy_{i+1}"][sample] = system.v[i][1]
            if config.dim > 2:
                data_frame[f"vz_{i+1}"][sample] = system.v[i][2]
        if config.get_acc:
            data_frame[f"ax_{i+1}"][sample] = acc[i][0]
            if config.dim > 1:
                data_frame[f"ay_{i+1}"][sample] = acc[i][1]
            if config.dim > 2:
                data_frame[f"az_{i+1}"][sample] = acc[i][2]


def plot_frame(data_frame, config, axes=[]):
    plt.plot(data_frame["x_1"], data_frame["y_1"], color="red")
    plt.plot(data_frame["x_2"], data_frame["y_2"], color="blue", marker='o')
    plt.plot(data_frame["x_3"], data_frame["y_3"], color="green")
    plt.savefig(config.config_name.with_suffix(".png"))
