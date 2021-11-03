from models.EstimateResult import EstimateResult


def print_estimate_result(estimate: EstimateResult):
    print(f"\n{estimate.estimate_type} оценка")
    print("\nФинальные вероятности состояний: ")
    for index in range(len(estimate.probabilities_list)):
        print(f"p{index}: {estimate.probabilities_list[index]}")

    print(f"\nВероятность отказа: {estimate.p_reject}")
    print(f"Среднее число заявок в очереди: {estimate.L_queue}")
    print(f"Среднее число заявок в системе: {estimate.L_system}")
    print(f"Относительная пропускная способность(Q): {estimate.Q}")
    print(f"Абсолютная пропускная способность(A):    {estimate.A}")
    print(f"Среднее время пребывания в системе: {estimate.t_system}")
    print(f"Среднее время пребывания в очереди: {estimate.t_queue}")
    print(f"Среднее число занятых каналов: {estimate.busy_channels}")