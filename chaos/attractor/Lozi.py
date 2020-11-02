from chaos.display import from_double_gen
from chaos.attractor import ITERATION


def f(x, y, a, b):
    return 1 - a * abs(x) + b * abs(y), x

def lozi_gen(a, b):
    x = 0.5
    y = 0
    for _ in range(ITERATION):
        yield x, y
        x, y = f(x, y, a, b)

def lozi(a=1.2, b=0.5):
    from_double_gen(lozi_gen, a, b)