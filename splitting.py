import numpy as np


def splitting(z, ggkp, t_ir, t_uv):
    data_size = len(z)
    average_ggkp = np.zeros(data_size)
    for ind in range(data_size):
        average_ggkp[ind] = np.average(ggkp[max(0, ind - int(t_ir / 2)):min(ind + int(t_ir / 2), data_size)])
    not_ir_ggkp = ggkp - average_ggkp
    not_ir_uv_ggkp = np.zeros(data_size)
    for ind in range(data_size):
        not_ir_uv_ggkp[ind] = np.average(not_ir_ggkp[max(0, ind - int(t_uv / 2)):min(ind + int(t_uv / 2), data_size)])

    borders = np.zeros(0)
    for ind in range(1, data_size):
        if not_ir_uv_ggkp[ind - 1] * not_ir_uv_ggkp[ind] < 0:
            borders = np.append(borders, z[ind])
    return borders
