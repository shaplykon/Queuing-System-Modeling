import math
from functools import reduce
import numpy as np


def get_theoretical_estimates(n, m, lambda_value, mu, v):
    # Коэффицент загрузки
    ro = lambda_value / mu
    beta = v / mu

    # Финальные вероятности состояний
    probabilities_list = []

    p0 = np.sum((math.pow(ro, i)) / (math.factorial(i)) for i in range(n + 1))

    sum = np.sum([ro ** i / reduce(
        lambda prod, x: prod * x, [(n + l * beta) for l in range(1, i + 1)]
    ) for i in range(1, m + 1)])

    p0 += ((math.pow(ro, n)) / (math.factorial(n))) * sum
    p0 = math.pow(p0, -1)

    probabilities_list.append(p0)

    for k in range(1, n + 1):
        probabilities_list.append((math.pow(ro, k) / math.factorial(k)) * p0)

    for i in range(1, m + 1):
        probabilities_list.append(probabilities_list[n - 1] * (
                math.pow(ro, i) / reduce(lambda prod, x: prod * x, [(n + l * beta) for l in range(1, i + 1)])))

    # Вероятность отказа
    p_reject = probabilities_list[n + m]

    # Относительная пропускная способность (вероятность обслуживания)
    Q = 1 - p_reject

    # Абсолютная пропускная способность
    A = lambda_value * Q

    # Среднее число заявок, находящихся в очереди
    L_queue = np.sum(i * probabilities_list[n + i] for i in range(1, m + 1))

    # Среднее число заявок, обслуживаемых в СМО
    L_system = np.sum(k * probabilities_list[k] for k in range(1, n + 1)) + np.sum(
        (n + i) * probabilities_list[n + i] for i in range(1, m + 1))

    # Среднее время пребывания в системе
    t_system = L_system / lambda_value

    # Среднее время пребывания в очереди
    t_queue = L_queue / lambda_value

    print("\nФинальные вероятности состояний: ")
    for index in range(len(probabilities_list)):
        print(f"p{index}: {probabilities_list[index]}")

    print(f"\nВероятность отказа: {p_reject}")
    print(f"Среднее число заявок в очереди: {L_queue}")
    print(f"Среднее число заявок в системе: {L_system}")
    print(f"Относительная пропускная способность(Q): {Q}")
    print(f"Абсолютная пропускная способность(A):    {A}")
    print(f"Среднее время пребывания в системе: {t_system}")
    print(f"Среднее время пребывания в очереди: {t_queue}")
