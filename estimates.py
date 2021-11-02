import math
from functools import reduce
import numpy as np

from EstimateResult import EstimateResult
from constants import *


def get_theoretical_estimates(n, m, lambda_value, mu, v) -> EstimateResult:
    estimate_result = EstimateResult()
    estimate_result.set_estimate_type(THEORETICAL_ESTIMATE)

    # Коэффицент загрузки
    ro = lambda_value / mu
    beta = v / mu

    # Финальные вероятности состояний
    estimate_result.probabilities_list = []

    p0 = np.sum((math.pow(ro, i)) / (math.factorial(i)) for i in range(n + 1))

    sum = np.sum([math.pow(ro, i) / reduce(
        lambda prod, x: prod * x, [(n + l * beta) for l in range(1, i + 1)]
    ) for i in range(1, m + 1)])

    p0 += ((math.pow(ro, n)) / (math.factorial(n))) * sum
    p0 = math.pow(p0, -1)

    estimate_result.probabilities_list.append(p0)

    for k in range(1, n + 1):
        estimate_result.probabilities_list.append((math.pow(ro, k) / math.factorial(k)) * p0)

    for i in range(1, m + 1):
        estimate_result.probabilities_list.append(estimate_result.probabilities_list[n - 1] * (
                math.pow(ro, i) / reduce(lambda prod, x: prod * x, [(n + l * beta) for l in range(1, i + 1)])))

    # Вероятность отказа
    estimate_result.p_reject = estimate_result.probabilities_list[n + m]

    # Относительная пропускная способность (вероятность обслуживания)
    estimate_result.Q = 1 - estimate_result.p_reject

    # Абсолютная пропускная способность
    estimate_result.A = lambda_value * estimate_result.Q

    # Среднее число заявок, находящихся в очереди
    estimate_result.L_queue = np.sum(i * estimate_result.probabilities_list[n + i] for i in range(1, m + 1))

    # Среднее число заявок, обслуживаемых в СМО
    estimate_result.L_system = np.sum(k * estimate_result.probabilities_list[k] for k in range(1, n + 1)) + np.sum(
        (n + i) * estimate_result.probabilities_list[n + i] for i in range(1, m + 1))

    # Среднее время пребывания в системе
    estimate_result.t_system = estimate_result.L_system / lambda_value

    # Среднее время пребывания в очереди
    estimate_result.t_queue = estimate_result.L_queue / lambda_value

    # Среднее число занятых каналов
    estimate_result.busy_channels = estimate_result.Q * ro

    return estimate_result
