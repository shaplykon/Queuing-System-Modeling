from display import *
from estimates import *
from constants import *
from simulation import *
from colorama import Fore


def run_system_simulation(show_additional_plots=False):
    for n, m, lambda_value, mu, v in TEST_DATA:
        simulation_results = []
        for simulation_time in SIMULATION_INTERVALS:
            environment = simpy.Environment()
            simulation_result = SimulationResult()
            system = QueuingSystem(n, m, lambda_value, mu, v, environment)
            environment.process(run_simulation(environment, simulation_result, system))
            environment.run(simulation_time)

            theoretical_result = get_theoretical_estimates(n, m, lambda_value, mu, v)
            empirical_result = get_empirical_estimates(simulation_result, system, simulation_time)
            comparative_result = compare_estimates(theoretical_result, empirical_result, simulation_time)

            # Вывод подсчитанных оценок только для последнего(самого продолжительного) интервала
            # симуляции. Остальные данные используются для построения графиков
            if simulation_time == SIMULATION_INTERVALS[len(SIMULATION_INTERVALS) - 1]:
                print(
                    f"\nСимуляции СМО с параметрами n={n}, m={m}, λ={lambda_value}, 𝜇={mu}, v={v} на временном "
                    f" интервале {simulation_time} мин.\n")
                print_estimate_result(theoretical_result)
                print_estimate_result(empirical_result)
                print_estimate_result(comparative_result)
            else:
                simulation_results.append(comparative_result)

        show_time_dependence_plot(simulation_results, system)

        # При выборе пользователем варианта с проведением анализа зависимости времени
        # заявки в очереди от интенсивности входного потока для системы производится симуляция с изменением
        # значения λ без изменения остальных параметров
        if show_additional_plots:
            lambda_simulation_results = []
            for test_lambda_value in range(1, 10):
                environment = simpy.Environment()
                simulation_result = SimulationResult()
                system = QueuingSystem(n, m, test_lambda_value, mu, v, environment)
                environment.process(run_simulation(environment, simulation_result, system))
                environment.run(SIMULATION_INTERVALS[len(SIMULATION_INTERVALS) - 1])
                empirical_result = get_empirical_estimates(simulation_result, system,
                                                           SIMULATION_INTERVALS[len(SIMULATION_INTERVALS) - 1])
                lambda_simulation_results.append(empirical_result)
            show_lambda_dependence_plot(lambda_simulation_results, system)


if __name__ == "__main__":
    user_input = input(f"\nПроизводить анализ зависимости времени \n"
                       f"заявки в очереди от интенсивности входного потока?(Y/N)\n{Fore.YELLOW}"
                       f"*увеличивает время выполнения{Fore.RESET}\n").upper()
    run_system_simulation(user_input == "Y")
