import simpy


class QueuingSystem:
    """
    Класс, представляющий модель системы массового обслуживания.
    """

    def __init__(self, n, m, lambda_value, mu, v, environment: simpy.Environment, k=1):
        """
        :param n: Число каналов
        :param m: Число мест в очереди
        :param lambda_value: Интенсивность потока заявок
        :param mu: Интенсивность потока обслуживания
        :param v: Параметр распределения для времени ожидания в очереди
        :param k: Порядок распределения Эрланга
        :param environment: Среда симуляции SimPy
        """
        self.n = n
        self.m = m
        self.lambda_value = lambda_value
        self.mu = mu
        self.v = v
        self.k = k
        self.environment = environment
        self.resource = simpy.Resource(self.environment, n)
