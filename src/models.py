"""
Модуль models.py: Модели данных, ООП (наследование, полиморфизм, композиция).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

# --- Пользовательские исключения ---
class HardwareError(Exception):
    """Базовое исключение для аппаратных ошибок."""
    pass

class IncompatibleHardwareError(HardwareError):
    """Ошибка несовместимости оборудования (например, разные сокеты)."""
    pass

# --- Модели комплектующих ---
@dataclass
class BaseComponent(ABC):
    """Абстрактный базовый класс компонента."""
    part_id: str
    model: str
    stock: int
    initial_price: float = field(repr=False) # Используется только для инициализации
    _price: float = field(init=False, repr=False, default=0.0)

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Сеттер с защитой состояния (запрет <= 0)."""
        if value <= 0:
            raise ValueError(f"Цена компонента '{self.model}' должна быть больше нуля.")
        self._price = value

    def __post_init__(self) -> None:
        """Срабатывает после инициализации датакласса для установки цены."""
        self.price = self.initial_price

    @abstractmethod
    def calculate_health_score(self) -> float:
        """Полиморфный метод для расчета состояния/износа."""
        pass

@dataclass
class Processor(BaseComponent):
    """Класс Процессора."""
    socket: str
    tdp: int

    def calculate_health_score(self) -> float:
        """Расчет состояния на основе тепловыделения (TDP)."""
        return max(0.0, 100.0 - (self.tdp / 2.0))

@dataclass
class StorageDrive(BaseComponent):
    """Класс Накопителя."""
    drive_type: str
    tbw_resource: int

    def calculate_health_score(self) -> float:
        """Расчет состояния на основе ресурса перезаписи (TBW)."""
        return min(100.0, self.tbw_resource / 10.0)

# --- Композиция ---
@dataclass
class PCBuild:
    """Класс Сборки ПК (демонстрирует композицию)."""
    build_id: str
    client_name: str
    components: List[BaseComponent] = field(default_factory=list)

    def add_component(self, component: BaseComponent) -> None:
        """Добавление компонента в сборку с проверкой на совместимость."""
        # Пример логики: если добавляем процессор, проверим, нет ли конфликта сокетов (упрощенно)
        existing_cpus = [c for c in self.components if isinstance(c, Processor)]
        if isinstance(component, Processor) and existing_cpus:
            if existing_cpus[0].socket != component.socket:
                raise IncompatibleHardwareError("В сборке не могут быть процессоры с разными сокетами!")
        self.components.append(component)

    def calculate_total_price(self) -> float:
        """Расчет общей стоимости сборки."""
        return sum(comp.price for comp in self.components)