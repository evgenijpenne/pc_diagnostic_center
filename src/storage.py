"""
Модуль storage.py: Работа с файлами (CSV, JSON), ленивая загрузка, потоки данных.
"""
import csv
import json
import logging
from typing import Generator, Dict, Any, List
from src.models import Processor, StorageDrive, BaseComponent

logger = logging.getLogger(__name__)


def read_hardware_csv_lazy(file_path: str) -> Generator[Dict[str, str], None, None]:
    """Генератор для ленивого (построчного) чтения CSV."""
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Поток данных: 1. Чтение
                yield row
    except FileNotFoundError as e:
        logger.error(f"Критическая ошибка: Файл '{file_path}' не найден.")
        raise e


def load_catalog(file_path: str) -> List[BaseComponent]:
    """
    Загрузка каталога.
    Поток: Чтение -> Проверка -> Преобразование -> Обработка
    """
    components = []

    try:
        for row in read_hardware_csv_lazy(file_path):
            # Поток данных: 2. Проверка (Validation)
            if not row.get('part_id') or not row.get('price'):
                logger.warning(f"Пропущена строка из-за неполных данных: {row}")
                continue

            try:
                # Поток данных: 3. Преобразование (Transformation)
                part_id = row['part_id']
                model = row['model']
                price = float(row['price'])
                stock = int(row['stock'])
                comp_type = row.get('type')

                # Поток данных: 4. Обработка (Processing - создание объектов)
                if comp_type == 'cpu':
                    comp = Processor(part_id, model, stock, price, row['socket'], int(row['tdp']))
                elif comp_type == 'storage':
                    comp = StorageDrive(part_id, model, stock, price, row['drive_type'], int(row['tbw']))
                else:
                    continue
                components.append(comp)

            except ValueError as ve:
                logger.warning(f"Ошибка значения (ValueError) в строке {row['part_id']}: {ve}")

    except FileNotFoundError:
        pass  # Ошибка уже залогирована в генераторе

    return components


def export_to_json(filepath: str, data: Dict[str, Any]) -> None:
    """Поток данных: 5. Запись в JSON."""
    try:
        with open(filepath, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logger.info(f"Успешный экспорт данных в {filepath}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении JSON: {e}")