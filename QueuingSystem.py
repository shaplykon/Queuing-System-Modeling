import simpy
import numpy as np


class QueuingSystem:
    """
    Класс, представляющий модель системы массового обслуживания.
    Содержит параметры СМО и методы для выполнения операций за время,
    зависящее от интенсивности потока осуживания
    """
    def __init__(self, n, m, lambda_value, mu, v, environment: simpy.Environment):
        """
        :param n: Число каналов
        :param m: Число мест в очереди
        :param lambda_value: Интенсивность потока заявок
        :param mu: Интенсивность потока обслуживания
        :param v: Параметр распределения
        :param environment: Среда симуляции SimPy
        """
        self.n = n
        self.m = m
        self.lambda_value = lambda_value
        self.mu = mu
        self.v = v
        self.environment = environment
        self.resource = simpy.Resource(self.environment, n)

    def action(self):
        yield self.environment.timeout(np.random.exponential(1 / self.mu))
