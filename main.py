from QueuingSystem import QueuingSystem
from display import print_estimate_result
from estimates import *
from constants import *
from simulation import *


def run_system_simulation():
    environment = simpy.Environment()
    environment.process(run_simulation(environment, 2, 2, 2, 1, 1))
    environment.run(SIMULATION_TIME)

    theoretical_result = get_theoretical_estimates(3, 4, 10, 3, 6)
    print_estimate_result(theoretical_result)


if __name__ == "__main__":
    run_system_simulation()



# get_theoretical_estimates(3, 4, 10, 3, 6)
