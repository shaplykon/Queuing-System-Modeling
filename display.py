from models import EstimateResult, QueuingSystem
from constants import COMPARATIVE_ESTIMATE, MU_SYMBOL, EPSILON, ERlANG_DISTRIBUTION_COEFFICIENTS
from colorama import Fore
import colorama
import matplotlib.pyplot as plt
import numpy as np

colorama.init(autoreset=True)


def show_erlang_coefficient_dependence_plot(empirical_estimates: list[EstimateResult], system: QueuingSystem):
    plt.title(f"Зависимость эмпирических характеристик СМО от порядка распределения Эрланга \nдля системы с"
              f" параметрами n={system.n}, m={system.m}, λ={system.lambda_value}, {MU_SYMBOL}={system.mu}, v={system.v}")

    plt.xlabel("Порядок распределения Эрланга(K)")
    plt.ylabel("Значения характеристик")

    plt.plot(ERlANG_DISTRIBUTION_COEFFICIENTS, [estimate.A for estimate in empirical_estimates], label=f"A")
    plt.plot(ERlANG_DISTRIBUTION_COEFFICIENTS, [estimate.Q for estimate in empirical_estimates], label=f"Q")
    plt.plot(ERlANG_DISTRIBUTION_COEFFICIENTS, [estimate.L_queue for estimate in empirical_estimates], label=f"Кол-во заявок в системе")
    plt.plot(ERlANG_DISTRIBUTION_COEFFICIENTS, [estimate.L_system for estimate in empirical_estimates], label=f"Кол-во заявок в системе")
    plt.plot(ERlANG_DISTRIBUTION_COEFFICIENTS, [estimate.t_system for estimate in empirical_estimates], label=f"Время в системе")
    plt.plot(ERlANG_DISTRIBUTION_COEFFICIENTS, [estimate.t_queue for estimate in empirical_estimates], label=f"Время в осереди")
    plt.plot(ERlANG_DISTRIBUTION_COEFFICIENTS, [estimate.p_reject for estimate in empirical_estimates],
             label=f"Вероятность отказа")

    plt.legend()
    plt.show()


def show_lambda_dependence_plot(empirical_estimates: list[EstimateResult], system: QueuingSystem):
    plt.title(f"График зависимости времени нахождения заявки в очереди от интенсивности\n"
              f" входного потока n={system.n}, m={system.m}, {MU_SYMBOL}={system.mu}, v={system.v}")

    plt.xlabel("Интенсивность потока заявок")
    plt.ylabel("Среднее время ожидания в очереди")

    plt.plot([estimate.A for estimate in empirical_estimates], [estimate.t_system for estimate in empirical_estimates],
             label=f"Время нахождения заявки в очереди")

    plt.legend()
    plt.show()


def show_time_dependence_plot(estimates_diff: list[EstimateResult], system: QueuingSystem):
    plt.title(f"Зависимость абсолютного отклонения оценок от продолжительности симуляции \nдля системы с"
              f" параметрами n={system.n}, m={system.m}, λ={system.lambda_value}, {MU_SYMBOL}={system.mu}, v={system.v}")

    plt.ylabel("Значение")
    plt.xlabel("Продолжительность симуляции(мин.)")

    time_intervals = [estimate.simulation_time for estimate in estimates_diff]

    plt.plot(time_intervals, [estimate.A for estimate in estimates_diff], label=f"A")
    plt.plot(time_intervals, [estimate.Q for estimate in estimates_diff], label=f"Q")
    plt.plot(time_intervals, [np.sum(estimate.probabilities_list) / len(estimate.probabilities_list)
                              for estimate in estimates_diff], label=f"Финальные вероятности")
    plt.plot(time_intervals, [estimate.p_reject for estimate in estimates_diff], label=f"Вероятность отказа")
    plt.plot(time_intervals, [estimate.busy_channels for estimate in estimates_diff], label=f"Число занятых каналов")

    plt.legend()
    plt.show()


def print_estimate_result(estimate: EstimateResult, is_single_channel=False):
    print(f"\n{estimate.estimate_type} оценка")
    if estimate.estimate_type == COMPARATIVE_ESTIMATE:
        print(Fore.YELLOW + "*значения абсолютных отклонений теоретической и эмпирической оценок")
    print("\nФинальные вероятности состояний: ")
    for index in range(len(estimate.probabilities_list)):
        print(f"p{index}: {estimate.probabilities_list[index]}")

    # При выводе сравнительной оценки(абсолютной разности теоретических и эспирических показателей)
    # сравниваем значения с epsilon для проверки корректности построения СМО
    if estimate.estimate_type == COMPARATIVE_ESTIMATE:
        print(f"\n{Fore.YELLOW}Значение ε: {EPSILON}")
        print(f"{Fore.GREEN if estimate.p_reject <= EPSILON else Fore.RED}\nВероятность отказа: {estimate.p_reject}")
        print(f"{Fore.GREEN if estimate.L_queue <= EPSILON else Fore.RED}Среднее число заявок в очереди: "
              f"{estimate.L_queue}")
        print(f"{Fore.GREEN if estimate.L_system <= EPSILON else Fore.RED}Среднее число заявок в системе: "
              f"{estimate.L_system}")
        print(f"{Fore.GREEN if estimate.Q <= EPSILON else Fore.RED}Относительная пропускная способность(Q): "
              f"{estimate.Q}")
        print(f"{Fore.GREEN if estimate.A <= EPSILON else Fore.RED}Абсолютная пропускная способность(A):    "
              f"{estimate.A}")
        print(f"{Fore.GREEN if estimate.t_system <= EPSILON else Fore.RED}Среднее время пребывания в системе: "
              f"{estimate.t_system}")
        print(f"{Fore.GREEN if estimate.t_queue <= EPSILON else Fore.RED}Среднее время пребывания в очереди: "
              f"{estimate.t_queue}")
        if not is_single_channel:
            print(f"{Fore.GREEN if estimate.busy_channels <= EPSILON else Fore.RED}Среднее число занятых каналов: "
                  f"{estimate.busy_channels}\n")

        try:
            assert estimate.p_reject <= EPSILON
            assert estimate.t_queue <= EPSILON
            assert estimate.t_system <= EPSILON
            assert estimate.A <= EPSILON
            assert estimate.Q <= EPSILON
            assert estimate.L_queue <= EPSILON
            assert estimate.L_system <= EPSILON
            if not is_single_channel:
                assert estimate.busy_channels <= EPSILON

            print(f"\n{Fore.GREEN}Смоделированная СМО НЕ превышает установленного абсолютного отклонения ε({EPSILON})")
        except AssertionError:
            print(
                f"\n{Fore.RED}Эмпирические характеристики СМО в результате моделирования имеют большее отклонение от\n"
                f"теоретических характеристик, чем установленное ε({EPSILON})")

    else:
        print(f"\nВероятность отказа: {estimate.p_reject}")
        print(f"Среднее число заявок в очереди: {estimate.L_queue}")
        print(f"Среднее число заявок в системе: {estimate.L_system}")
        print(f"Относительная пропускная способность(Q): {estimate.Q}")
        print(f"Абсолютная пропускная способность(A):    {estimate.A}")
        print(f"Среднее время пребывания в системе: {estimate.t_system}")
        print(f"Среднее время пребывания в очереди: {estimate.t_queue}")
        print(f"Среднее число занятых каналов: {estimate.busy_channels}")
