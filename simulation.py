import simpy as simpy
import numpy as np
from QueuingSystem import QueuingSystem


def simulate(env: simpy.Environment, system: QueuingSystem):
    time = env.now

    with system.resource.request() as request:
        yield request
        yield env.process(system.action())


def run_simulation(env: simpy.Environment, n, m, lambda_value, mu, v):
    system = QueuingSystem(n, m, lambda_value, mu, v, env)
    timeout_value = np.random.exponential(1 / system.lambda_value)

    while True:
        yield env.timeout(timeout_value)
        env.process(simulate(env, system))
