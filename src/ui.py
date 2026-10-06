"""
Модуль ui.py: Текстовое интерактивное CLI-меню.
"""
from src.models import BaseComponent, PCBuild
from src.services import DiagnosticCenter
from src.storage import export_to_json
from typing import Any


def start_ui(service: DiagnosticCenter) -> None:
    active_builds: list[PCBuild] = []

    while True:
        print("\n=== PC Assembly & Diagnostic Center ===")
        print("1. Показать каталог комплектующих (по возрастанию цены)")
        print("2. Найти деталь (Усовершенствованный бинарный поиск)")
        print("3. Собрать новый ПК (Композиция)")
        print("4. Передать ПК на диагностику (Очередь)")
        print("5. Провести диагностику (Извлечь из очереди)")
        print("6. Экспорт состояния в JSON и выход")
        print("=======================================")

        choice: str = input("Выберите действие: ")

        if choice == '1':
            sorted_cat: list[BaseComponent] = service.get_sorted_catalog_by_price()
            print("\nКаталог комплектующих:")
            for c in sorted_cat:
                print(f"[{c.part_id}] {c.model} - {c.price}$ (Здоровье: {c.calculate_health_score()}%)")

        elif choice == '2':
            search_query: str = input("Введите точный ID или начало ID (например, 'CPU', 'SSD', 'CPU03'): ")
            found_comps: list[BaseComponent] = service.search_components(search_query)
            if found_comps:
                print(f"\nНайдено совпадений: {len(found_comps)}")
                for comp in found_comps:
                    print(f"  -> [{comp.part_id}] {comp.model} за {comp.price}$")
            else:
                print("Компоненты по такому запросу не найдены.")

        elif choice == '3':
            b_id: str = input("ID сборки (например, PC-1): ")
            c_name: str = input("Имя клиента: ")
            build: PCBuild = PCBuild(b_id, c_name)

            p_id: str = input("Введите ТОЧНЫЙ ID процессора для добавления (например, CPU01): ")
            cpu: BaseComponent | None = service.find_component_by_id_exact(p_id)
            if cpu:
                try:
                    build.add_component(cpu)
                    active_builds.append(build)
                    print(f"Успех! Общая стоимость ПК: {build.calculate_total_price()}$")
                except Exception as e:
                    print(f"Ошибка при сборке: {e}")
            else:
                print("Процессор с таким точным ID не найден.")

        elif choice == '4':
            if not active_builds:
                print("Нет собранных ПК. Сначала соберите ПК (пункт 3).")
                continue
            target_build_id: str = active_builds[-1].build_id
            service.enqueue_pc(target_build_id)
            print(f"Сборка '{target_build_id}' добавлена в очередь на диагностику.")

        elif choice == '5':
            diag_pc: str | None = service.dequeue_pc()
            if diag_pc:
                print(f"Диагностика ПК '{diag_pc}' завершена.")
            else:
                print("Очередь на диагностику пуста.")

        elif choice == '6':
            state: dict[str, Any] = {
                "supported_sockets": list(service.supported_sockets),
                "builds": [{"id": b.build_id, "price": b.calculate_total_price()} for b in active_builds]
            }
            export_to_json("pc_service_db.json", state)
            print("Состояние сохранено. Выход...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")