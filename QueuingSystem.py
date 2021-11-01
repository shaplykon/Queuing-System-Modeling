class QueuingSystem:
    def __init__(self, n, m, lambda_value, mu, v):
        self.n = n                              # Число каналов
        self.m = m                              # Число меств очереди
        self.lambda_value = lambda_value        # Интенсивность потока заявок
        self.mu = mu                            # Интенсивность потока обслуживания
        self.v = v                              # Параметр распределения


