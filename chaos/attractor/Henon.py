from chaos.display import from_double_gen


def f(x, y, a, b):
    return y + 1 - a * x * x, b * x

def henon_gen(a, b):
    x = 0.5
    y = 0
    for _ in range(1000):
        yield x, y
        x, y = f(x, y, a, b)

def henon(a=1.4, b=0.3):
    from_double_gen(henon_gen, a, b)

