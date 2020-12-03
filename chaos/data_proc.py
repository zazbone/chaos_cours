import pandas as pd

from pathlib import Path

import matplotlib.pyplot as plt


def plot_xy(file, x_name, y_name):
    file_path = Path(file)
    data = pd.read_csv(file_path.with_suffix(".csv"), names=[x_name, y_name])
    print(data.head(5)[[x_name, y_name]])
    data[[x_name, y_name]].plot()
