import math
import logging as log

T = 85  # Количество регионов
N = 67896500  # Население?
FILENAME = 'data.tsv'

log.basicConfig(level='INFO')


def read_file(filename):
    x_arr, m_arr = [], []
    with open(filename, mode='r', encoding='utf-8') as file:
        log.info("1")
        file.readline()
        for line in file:
            vals = line.split('\t')
            x_str = vals[1] \
                .replace('\xa0', '') \
                .replace('\n', '') \
                .replace(',', '.')
            x_arr.append(float(x_str))
            m_str = vals[2] \
                .replace('\xa0', '') \
                .replace('\n', '') \
                .replace(',', '.')
            m_arr.append(float(m_str))
    return x_arr, m_arr


def f(a, x_arr, m_arr):
    var_1 = sum([x_arr[i] * m_arr[i] for i in range(T)]) / N
    var_2 = 1 / a
    var_3 = sum([x_arr[i] * math.exp(a * x_arr[i]) * m_arr[i] for i in range(T)]) / N
    var_4 = sum([math.exp(a * x_arr[i]) * m_arr[i] for i in range(T)]) / N
    return var_1 + var_2 - var_3 / (var_4 - 1)


def get_b(a, x_arr, m_arr):
    var_1 = sum([m_arr[i] / N * math.exp(a * x_arr[i]) for i in range(T)]) - 1
    print("%.10f" % var_1)
    return a / var_1


def main():
    x_arr, m_arr = read_file(FILENAME)
    log.info(f'x = {x_arr}')
    log.info(f'm = {m_arr}')
    a_1, a_2 = 0.1, 0.1 - 10 ** -4
    while abs(a_2 - a_1) > 0.000001:
        var_1 = 1 / (1 - f(a_1, x_arr, m_arr) / f(a_2, x_arr, m_arr))
        var_2 = a_2 - a_1
        log.info(f"{a_2 * var_1 * var_2}")
        a_1, a_2 = a_2, a_2 - var_1 * var_2
    log.info(f"Альфа:  %.20f" % a_2)
    log.info(f"B:      %.20f" % get_b(a_2, x_arr, m_arr))


if __name__ == '__main__':
    main()
