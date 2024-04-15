import numpy as np

# функция сначала делает усреднение по t_ir точкам и вычитает из текущего массива данных усредненыый. По сути это эквивалентно
# обрезанию низких частот в фурье. После этого она проводит усреднение по t_uv точкам, что эквивалентно обрезанию высоких
# частот фурье. В конце она смотрит пересечение результата с 0 и выдает координаты этих пересечений. Эти пересечения
# довольно хорошо совпадают с разбиением на участки от геолога.
def splitting(z, ggkp, t_ir=201, t_uv=11):
    data_size = len(z)
    average_ggkp = np.zeros(data_size)

    # обрезаем низкие частоты
    for ind in range(data_size):
        average_ggkp[ind] = np.average(ggkp[max(0, ind - int(t_ir / 2)):min(ind + int(t_ir / 2), data_size)])
    not_ir_ggkp = ggkp - average_ggkp

    # обрезаем высокие частоты
    not_ir_uv_ggkp = np.zeros(data_size)
    for ind in range(data_size):
        not_ir_uv_ggkp[ind] = np.average(not_ir_ggkp[max(0, ind - int(t_uv / 2)):min(ind + int(t_uv / 2), data_size)])

    # botv gthtctxtybz c 0 -- они будут нашими границами участков классов
    borders = np.zeros(0)
    for ind in range(1, data_size):
        if not_ir_uv_ggkp[ind - 1] * not_ir_uv_ggkp[ind] < 0:
            borders = np.append(borders, z[ind])
    return borders
