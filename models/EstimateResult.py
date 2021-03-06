from dataclasses import dataclass, field


@dataclass
class EstimateResult:
    """
    Класс, представляющий модель данных, возвращаемую в результате
    подсчёта характеристик СМО.
    """
    estimate_type: str = field(default="")
    simulation_time: int = field(default=0)
    probabilities_list: list[int] = field(default_factory=list)
    p_reject: float = field(default=0)
    L_queue: float = field(default=0)
    L_system: float = field(default=0)
    Q: float = field(default=0)
    A: float = field(default=0)
    t_system: float = field(default=0)
    t_queue: float = field(default=0)
    busy_channels: float = field(default=0)

    def set_estimate_type(self, estimate_type):
        self.estimate_type = estimate_type

