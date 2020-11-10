def step(func, t, h, y, **kwargs):
    """\
    4rd ordre Runge-kutta algorithm implémentation
    Compute only one step

    func: function to integrate
    x: variable to integrate around
    delta_x: width of the integral
    *args: additionnal arguments for the function\
    """
    k1 = func(t, y, **kwargs)
    k2 = func(t + 0.5 * h, y + 0.5 * h * k1, **kwargs)
    k3 = func(t + 0.5 * h, y + 0.5 * h * k2, **kwargs)
    k4 = func(t + h, y + h * k3, **kwargs)
    a = 1 / 3
    b = 1 / 6
    return h * (b * k1 + a * k2 + a * k3 + b * k4)


if __name__ == "__main__":
    from math import sin, pi, pow
    import matplotlib.pyplot as plt

    class Mobil:
        def __init__(self, lenth, mass, init_angle, init_speed, t0, dt, sample):
            self.mass = mass
            self.lenth = lenth

            self.angle = (init_angle / 360) * 2 * pi
            self.speed = (init_speed / 360) * 2 * pi

            self.t = t0
            self.dt = dt
            self.tf = t0 + dt * sample

        @staticmethod
        def pendulum_acc(t, angle, g, lenth):
            # Time does not interfer
            return -(g / lenth) * sin(angle)

        def p(self):
            return pow(self.speed * self.lenth, 2) * self.mass

        def __iter__(self):
            return self

        def __next__(self):
            # self.speed += type(self).pendulum_acc(self.t, self.angle, 1, self.lenth) * dt
            # Runge Kutta integral
            self.speed += step(
                func=type(self).pendulum_acc,
                t=self.t,
                h=self.dt,
                y=self.angle,
                g=9.81,
                lenth=self.lenth
            )
            # Simple Euler method, x = int(dx/dt) trivial
            self.angle += self.speed * self.dt
            self.t += dt

            if self.tf < self.t:
                raise StopIteration

            return self.speed, self.angle, self.t

    init_angle = 20 - 90  # degres
    init_speed = 0

    t0 = 0
    dt = 0.01
    sample = 400

    mobil = Mobil(1, 0.1, init_angle, init_speed, t0, dt, sample)

    time_axes = [t0]
    speed_axes = [(init_speed / 360) * 2 * pi]
    angle_axes = [(init_angle / 360) * 2 * pi]
    y_axes = [sin(init_angle) * mobil.lenth]

    for ang_sp, ang, t in mobil:
        speed_axes.append(ang_sp)
        angle_axes.append(ang)
        time_axes.append(t)
        y_axes.append(sin(ang) * mobil.lenth)
        print(t)

    plt.plot(speed_axes, angle_axes)
    plt.show()
