"""
Модуль test_core.py: Юнит-тесты для проверки логики, ООП и алгоритмов.
"""
import unittest
from src.models import Processor, StorageDrive, PCBuild, IncompatibleHardwareError
from src.services import quick_sort, enhanced_binary_search


class TestModelsAndOOP(unittest.TestCase):
    """Тестирование ООП, инкапсуляции и полиморфизма."""

    def test_price_validation(self) -> None:
        """Проверка защиты состояния: запрет цены <= 0."""
        with self.assertRaises(ValueError):
            Processor(part_id="CPU99", model="Test CPU", stock=5, initial_price=-100.0, socket="AM4", tdp=65)

    def test_polymorphism_health_score(self) -> None:
        """Проверка полиморфного расчета состояния здоровья."""
        cpu = Processor(part_id="CPU01", model="Test CPU", stock=5, initial_price=100.0, socket="AM4", tdp=100)
        ssd = StorageDrive(part_id="SSD01", model="Test SSD", stock=5, initial_price=50.0, drive_type="NVMe", tbw_resource=600)

        # Для CPU: 100 - (100 / 2) = 50.0
        self.assertEqual(cpu.calculate_health_score(), 50.0)
        # Для SSD: 600 / 10 = 60.0
        self.assertEqual(ssd.calculate_health_score(), 60.0)

    def test_incompatible_hardware_exception(self) -> None:
        """Проверка выбрасывания IncompatibleHardwareError при разных сокетах."""
        build = PCBuild(build_id="PC-01", client_name="Иван")
        cpu1 = Processor(part_id="CPU01", model="CPU 1", stock=1, initial_price=100.0, socket="AM4", tdp=65)
        cpu2 = Processor(part_id="CPU02", model="CPU 2", stock=1, initial_price=150.0, socket="LGA1700", tdp=65)

        build.add_component(cpu1)
        with self.assertRaises(IncompatibleHardwareError):
            build.add_component(cpu2)


class TestAlgorithms(unittest.TestCase):
    """Тестирование пользовательских алгоритмов."""

    def test_quick_sort(self) -> None:
        """Проверка работы кастомного QuickSort."""
        numbers = [5, 1, 9, 3, 7]
        sorted_numbers = quick_sort(numbers)
        self.assertEqual(sorted_numbers, [1, 3, 5, 7, 9])

    def test_enhanced_binary_search(self) -> None:
        """Проверка усовершенствованного бинарного поиска."""
        cpu1 = Processor(part_id="CPU01", model="CPU 1", stock=1, initial_price=100.0, socket="AM4", tdp=65)
        cpu2 = Processor(part_id="CPU02", model="CPU 2", stock=1, initial_price=150.0, socket="AM4", tdp=65)
        ssd = StorageDrive(part_id="SSD01", model="SSD 1", stock=1, initial_price=50.0, drive_type="NVMe", tbw_resource=300)

        sorted_catalog = [cpu1, cpu2, ssd]  # Отсортировано по part_id

        # Поиск по префиксу 'CPU' должен вернуть 2 процессора
        results = enhanced_binary_search(sorted_catalog, "CPU")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].part_id, "CPU01")
        self.assertEqual(results[1].part_id, "CPU02")

        # Поиск несуществующего элемента
        empty_results = enhanced_binary_search(sorted_catalog, "RAM")
        self.assertEqual(len(empty_results), 0)


if __name__ == '__main__':
    unittest.main()