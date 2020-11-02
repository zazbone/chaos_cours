def four_order(func, step: int, init_time: float, end_time: float, *arg):
    """\
        func: function that represente differential equation to studie
              func need to take a time argument (t=) and additionnal dimensional argument (*arg)
              q_i'= f(t, q_1, q_2, ..., q_i, ..., q_n)
              time may not intervene in differential equation
        step: number of step to compute
        init_time: t_0
        end_time: t_f
    """
    pass