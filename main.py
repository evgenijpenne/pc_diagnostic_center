"""
main.py: Точка входа в приложение.
"""
import csv
import logging
import os
from src.models import BaseComponent
from src.services import DiagnosticCenter
from src.storage import load_catalog
from src.ui import start_ui

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()]
)
logger: logging.Logger = logging.getLogger("MAIN")


def create_mock_csv(filepath: str) -> None:
    """Генерация расширенного тестового CSV-файла."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Пересоздаем файл с большим каталогом комплектующих
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['part_id', 'type', 'model', 'price', 'stock', 'socket', 'tdp', 'drive_type', 'tbw'])

        # --- Процессоры (CPU) ---
        writer.writerow(['CPU01', 'cpu', 'Intel Core i9-13900K', '580.0', '8', 'LGA1700', '125', '', ''])
        writer.writerow(['CPU02', 'cpu', 'AMD Ryzen 7 7800X3D', '440.0', '15', 'AM5', '120', '', ''])
        writer.writerow(['CPU03', 'cpu', 'Intel Core i5-13400F', '200.0', '20', 'LGA1700', '65', '', ''])
        writer.writerow(['CPU04', 'cpu', 'AMD Ryzen 5 5600', '130.0', '30', 'AM4', '65', '', ''])
        writer.writerow(['CPU05', 'cpu', 'Intel Core i3-12100F', '95.0', '25', 'LGA1700', '58', '', ''])
        writer.writerow(['CPU06', 'cpu', 'AMD Ryzen 9 7950X', '550.0', '5', 'AM5', '170', '', ''])
        # Тестовая строка с некорректной ценой для проверки валидации
        writer.writerow(['CPU07', 'cpu', 'Braked Pentium', '-30.0', '2', 'LGA1200', '50', '', ''])

        # --- Накопители (Storage Drives) ---
        writer.writerow(['SSD01', 'storage', 'Samsung 980 Pro 1TB', '110.0', '40', '', '', 'NVMe', '600'])
        writer.writerow(['SSD02', 'storage', 'Kingston NV2 500GB', '45.0', '60', '', '', 'NVMe', '160'])
        writer.writerow(['SSD03', 'storage', 'Crucial MX500 1TB', '80.0', '25', '', '', 'SATA', '360'])
        writer.writerow(['SSD04', 'storage', 'WD Black SN850X 2TB', '160.0', '12', '', '', 'NVMe', '1200'])
        writer.writerow(['HDD01', 'storage', 'Seagate BarraCuda 2TB', '55.0', '35', '', '', 'HDD', '300'])
        writer.writerow(['HDD02', 'storage', 'WD Blue 4TB', '90.0', '18', '', '', 'HDD', '450'])

    logger.info(f"Обновлен CSV-файл каталога: {filepath}")


if __name__ == "__main__":
    csv_path: str = "data/hardware_catalog.csv"

    # При каждом запуске файл пересоздается с новым каталогом
    create_mock_csv(csv_path)

    service: DiagnosticCenter = DiagnosticCenter()
    logger.info("Загрузка данных из каталога...")
    catalog: list[BaseComponent] = load_catalog(csv_path)

    for comp in catalog:
        service.register_component(comp)

    logger.info(f"Загружено {len(service.catalog_list)} валидных компонентов.")

    try:
        start_ui(service)
    except KeyboardInterrupt:
        logger.info("Приложение принудительно завершено пользователем.")