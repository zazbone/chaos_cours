import numpy as np


def coef(deriv_fn, values):
    values = np.array(values)
    der_values = deriv_fn(values)
    abs_values = abs(der_values)
    log_values = np.log(abs_values)
    n = len(log_values)
    sum_values = np.sum(log_values)
    return sum_values / n
