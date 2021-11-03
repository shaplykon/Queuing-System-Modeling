from display import print_estimate_result
from estimates import *
from constants import *
from simulation import *


def run_system_simulation():
    for n, m, lambda_value, mu, v in TEST_DATA:
        print(
            f"\nСимуляции СМО с параметрами n={n}, m={m}, λ={lambda_value}, 𝜇={mu}, v={v} на временном интервале "
            f"{SIMULATION_TIME} мин.")

        environment = simpy.Environment()
        simulation_result = SimulationResult()
        system = QueuingSystem(n, m, lambda_value, mu, v, environment)
        environment.process(run_simulation(environment, simulation_result, system))
        environment.run(SIMULATION_TIME)

        theoretical_result = get_theoretical_estimates(n, m, lambda_value, mu, v)
        empirical_result = get_empirical_estimates(simulation_result, system)

        print_estimate_result(theoretical_result)
        print_estimate_result(empirical_result)

        print_estimate_result(compare_estimates(theoretical_result, empirical_result))


if __name__ == "__main__":
    run_system_simulation()

# get_theoretical_estimates(3, 4, 10, 3, 6)
