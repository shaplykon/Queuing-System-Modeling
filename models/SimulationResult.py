from dataclasses import dataclass, field


@dataclass
class SimulationResult:
    """
    Класс, представляющий модель данных, возвращаемую в результате
    проведения симуляции СМО. Содержит эмпирические значения характеристик.
    """
    processed_requests: int = field(default=0)
    common_requests: int = field(default=0)
    busy_channels: list[int] = field(default_factory=list)
    count_requests_in_system: list[int] = field(default_factory=list)
    count_requests_in_queue: list[int] = field(default_factory=list)
    time_requests_in_queue: list[int] = field(default_factory=list)
    time_requests_in_system: list[int] = field(default_factory=list)