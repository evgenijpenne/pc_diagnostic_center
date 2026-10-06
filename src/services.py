"""
Модуль services.py: Алгоритмы и структуры данных.
"""
from collections import deque
from collections.abc import Callable
from typing import Any
from src.models import BaseComponent, Processor


def quick_sort(arr: list[Any], key: Callable[[Any], Any] = lambda x: x) -> list[Any]:
    """Быстрая сортировка QuickSort. Сложность O(n log n)."""
    if len(arr) <= 1:
        return arr
    pivot: Any = key(arr[len(arr) // 2])
    left: list[Any] = [x for x in arr if key(x) < pivot]
    middle: list[Any] = [x for x in arr if key(x) == pivot]
    right: list[Any] = [x for x in arr if key(x) > pivot]
    return quick_sort(left, key) + middle + quick_sort(right, key)


def enhanced_binary_search(arr: list[BaseComponent], target: str) -> list[BaseComponent]:
    """
    Усовершенствованный бинарный поиск.
    1. Классический бинарный поиск O(log n) для нахождения точки входа.
    2. Двунаправленное расширение O(k) для сбора всех совпадений (точных или по префиксу).
    """
    low: int = 0
    high: int = len(arr) - 1
    found_idx: int = -1

    # Этап 1: Классический бинарный поиск
    while low <= high:
        mid: int = (low + high) // 2
        mid_id: str = arr[mid].part_id

        if mid_id.startswith(target):
            found_idx = mid
            break  # Нашли базовое совпадение, останавливаем стандартный поиск
        elif mid_id < target:
            low = mid + 1
        else:
            high = mid - 1

    if found_idx == -1:
        return []

    # Этап 2: Усовершенствование (сбор всех элементов вокруг найденного)
    results: list[BaseComponent] = []

    # Идем влево от найденного индекса
    left: int = found_idx
    while left >= 0 and arr[left].part_id.startswith(target):
        results.insert(0, arr[left])
        left -= 1

    # Идем вправо от найденного индекса (не включая сам found_idx)
    right: int = found_idx + 1
    while right < len(arr) and arr[right].part_id.startswith(target):
        results.append(arr[right])
        right += 1

    return results


class DiagnosticCenter:
    """Сервис для управления бизнес-логикой."""

    def __init__(self) -> None:
        self.catalog_list: list[BaseComponent] = []
        self.catalog_index: dict[str, BaseComponent] = {}
        self.supported_sockets: set[str] = set()
        self.diagnostic_queue: deque[str] = deque()

    def register_component(self, component: BaseComponent) -> None:
        self.catalog_list.append(component)
        self.catalog_index[component.part_id] = component
        if isinstance(component, Processor):
            self.supported_sockets.add(component.socket)

    def get_sorted_catalog_by_price(self) -> list[BaseComponent]:
        return quick_sort(self.catalog_list, key=lambda c: c.price)

    def search_components(self, query: str) -> list[BaseComponent]:
        """Использование усовершенствованного бинарного поиска."""
        # Для бинарного поиска обязательна предварительная сортировка по ID
        sorted_by_id: list[BaseComponent] = quick_sort(self.catalog_list, key=lambda c: c.part_id)
        return enhanced_binary_search(sorted_by_id, query.upper())

    def find_component_by_id_exact(self, part_id: str) -> BaseComponent | None:
        """Поиск O(1) через hash-map для внутренних нужд (сборка ПК)."""
        return self.catalog_index.get(part_id.upper())

    def enqueue_pc(self, build_id: str) -> None:
        self.diagnostic_queue.append(build_id)

    def dequeue_pc(self) -> str | None:
        if self.diagnostic_queue:
            return self.diagnostic_queue.popleft()
        return None