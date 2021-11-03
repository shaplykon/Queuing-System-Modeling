import simpy as simpy
import numpy as np
from models.QueuingSystem import QueuingSystem
from models.SimulationResult import SimulationResult


def simulate(env: simpy.Environment, system: QueuingSystem, simulation_result: SimulationResult):
    time = env.now

    with system.resource.request() as request:
        # Фиксирование общего количества заявок, занятых каналов и заявок в СМО
        simulation_result.common_requests += 1
        simulation_result.busy_channels.append(len(system.resource.users) + len(system.resource.queue))
        simulation_result.count_requests_in_system.append(system.resource.count + len(system.resource.queue) - 1)

        # Вход в систему при наличии мест в очереди
        if system.m >= len(system.resource.queue):
            simulation_result.count_requests_in_queue.append(len(system.resource.queue))

            # Ожидание освобождения ресурса или выход из очереди(по истечении времени пребывания в очереди)
            result = yield request | env.timeout(np.random.exponential(1 / system.v))

            # Фиксирование времени заявки в очереди вне зависимости от результата ожидания(особождения
            # ресурса или окончания времени пребывания в очереди)
            simulation_result.time_requests_in_queue.append(env.now - time)

            # Обслуживание заявки
            if request in result:
                yield env.timeout(np.random.exponential(1 / system.mu))
            simulation_result.processed_requests += 1
        else:
            simulation_result.count_requests_in_queue.append(system.m)
            simulation_result.time_requests_in_queue.append(0)

        simulation_result.time_requests_in_system.append(env.now - time)


def run_simulation(env: simpy.Environment, simulation_result: SimulationResult, system: QueuingSystem):
    while True:
        timeout_value = np.random.exponential(1 / system.lambda_value)
        yield env.timeout(timeout_value)
        env.process(simulate(env, system, simulation_result))
