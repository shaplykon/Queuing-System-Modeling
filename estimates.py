import math
from functools import reduce
import numpy as np

from models.EstimateResult import EstimateResult
from models.QueuingSystem import QueuingSystem
from models.SimulationResult import SimulationResult
from constants import *


def get_empirical_estimates(simulation_result: SimulationResult, system: QueuingSystem, simulation_time: int):
    estimate_result = EstimateResult()
    estimate_result.set_estimate_type(EMPIRICAL_ESTIMATE)

    estimate_result.p_reject = (simulation_result.common_requests -
                                simulation_result.processed_requests) / simulation_result.common_requests

    estimate_result.A = simulation_result.processed_requests / simulation_time

    for probability_index in range(system.n + system.m + 1):
        estimate_result.probabilities_list.append(
            simulation_result.busy_channels.count(probability_index + 1) / len(simulation_result.busy_channels))

    # Среднее количество заявок в очереди на основании финальных вероятностей состояний
    # с соответствующими весами
    probability_weight = 0
    for index in range(system.n, system.m + system.n + 1):
        estimate_result.L_queue += (probability_weight * estimate_result.probabilities_list[index])
        probability_weight += 1

    estimate_result.L_system = np.sum(simulation_result.count_requests_in_system) / len(
        simulation_result.count_requests_in_system)

    estimate_result.t_queue = np.sum(simulation_result.time_requests_in_queue) / simulation_result.common_requests
    estimate_result.t_system = np.sum(simulation_result.time_requests_in_system) / simulation_result.common_requests

    estimate_result.busy_channels = estimate_result.L_system

    # Относительная пропускная способность (вероятность обслуживания)
    estimate_result.Q = 1 - estimate_result.p_reject
    return estimate_result


def get_theoretical_estimates_for_multi_channel(n, m, lambda_value, mu, v) -> EstimateResult:
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
        estimate_result.probabilities_list.append(estimate_result.probabilities_list[n] * (
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


def get_theoretical_estimates_for_single_channel(m, lambda_value, mu, k):
    estimate_result = EstimateResult()
    estimate_result.set_estimate_type(THEORETICAL_ESTIMATE)

    mu = mu / k

    # Коэффицент загрузки
    ro = lambda_value / mu

    estimate_result.probabilities_list.append((1 - ro) / (1 - math.pow(ro, m + 2)))

    for i in range(1, m + 2):
        estimate_result.probabilities_list.append(math.pow(ro, i) * estimate_result.probabilities_list[0])

    estimate_result.p_reject = estimate_result.probabilities_list[m + 1]

    estimate_result.Q = 1 - estimate_result.p_reject
    estimate_result.A = lambda_value * estimate_result.Q

    for i in range(1, m + 1):
        estimate_result.L_queue += (i * estimate_result.probabilities_list[i + 1])

    estimate_result.L_system = ro * estimate_result.Q + estimate_result.L_queue

    estimate_result.t_system = estimate_result.L_system / lambda_value

    estimate_result.t_queue = estimate_result.L_queue / lambda_value

    return estimate_result


def compare_estimates(theoretical: EstimateResult, empirical: EstimateResult, simulate_time: int) -> EstimateResult:
    estimates_diff = EstimateResult()
    estimates_diff.estimate_type = COMPARATIVE_ESTIMATE
    estimates_diff.simulation_time = simulate_time

    estimates_diff.probabilities_list = np.absolute(
        np.subtract(theoretical.probabilities_list, empirical.probabilities_list))
    estimates_diff.p_reject = math.fabs(empirical.p_reject - theoretical.p_reject)
    estimates_diff.Q = math.fabs(empirical.Q - theoretical.Q)
    estimates_diff.A = math.fabs(empirical.A - theoretical.A)
    estimates_diff.busy_channels = math.fabs(empirical.busy_channels - theoretical.busy_channels)
    estimates_diff.t_queue = math.fabs(empirical.t_queue - theoretical.t_queue)
    estimates_diff.t_system = math.fabs(empirical.t_system - theoretical.t_system)
    estimates_diff.L_queue = math.fabs(empirical.L_queue - theoretical.L_queue)
    estimates_diff.L_system = math.fabs(empirical.L_system - theoretical.L_system)

    return estimates_diff
