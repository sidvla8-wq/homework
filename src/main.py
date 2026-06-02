from typing import Any, Dict, List

from bank_operations import filter_by_status, filter_ruble_transactions, process_bank_search, sort_by_date
from data_loader import load_csv_data, load_json_data, load_xlsx_data


def load_data_from_file(choice: str) -> List[Dict[str, Any]]:
    """Загрузка данных из файла выбранного формата"""
    file_path = input("Введите путь к файлу: ")
    try:
        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            return load_json_data(file_path)
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            return load_csv_data(file_path)
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            return load_xlsx_data(file_path)
        else:
            raise ValueError("Неверный выбор формата файла")
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return []


def get_valid_status() -> str:
    """Получение корректного статуса от пользователя с повторным запросом при ошибке"""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = (
            input(
                "Введите статус, по которому необходимо выполнить фильтрацию.\n"
                "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
            )
            .strip()
            .upper()
        )
        if status in valid_statuses:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status
        else:
            print(f'Статус операции "{status}" недоступен.')


def get_sort_parameters() -> tuple[bool, bool]:
    """Получение параметров сортировки от пользователя"""
    sort_choice = input("Отсортировать операции по дате? Да/Нет\n").strip().lower()
    if sort_choice in ["да", "yes", "y"]:
        order_choice = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        ascending = order_choice in ["по возрастанию", "возрастание", "asc", "ascending"]
        return True, ascending
    return False, True


def should_filter_ruble() -> bool:
    """Запрос на фильтрацию рублёвых транзакций"""
    choice = input("Выводить только рублевые транзакции? Да/Нет\n").strip().lower()
    return choice in ["да", "yes", "y"]


def get_search_term() -> str:
    """Получение строки для поиска в описании"""
    search_choice = (
        input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower()
    )
    if search_choice in ["да", "yes", "y"]:
        return input("Введите строку для поиска: ").strip()
    return ""


def format_operation(operation: Dict[str, Any]) -> str:
    """Форматирование операции для вывода в консоль"""
    date = operation.get("date", "Не указана")
    desc = operation.get("description", "Без описания")
    amount = operation.get("amount", "Не указана")
    account_from = operation.get("from", "")
    account_to = operation.get("to", "")

    formatted = f"{date} {desc}\n"
    if account_from or account_to:
        from_part = account_from if account_from else "Не указан"
        to_part = account_to if account_to else "Не указан"
        formatted += f"{from_part} -> {to_part}\n"
    formatted += f"Сумма: {amount}\n"
    return formatted


def main():
    """Основная функция программы"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор формата файла
    file_choice = input().strip()
    data = load_data_from_file(file_choice)

    if not data:
        print("Не удалось загрузить данные. Завершение работы.")
        return

    # Фильтрация по статусу
    status = get_valid_status()
    filtered_data = filter_by_status(data, status)

    # Сортировка по дате
    sort_needed, ascending = get_sort_parameters()
    if sort_needed:
        filtered_data = sort_by_date(filtered_data, ascending)

    # Фильтрация рублёвых транзакций
    if should_filter_ruble():
        filtered_data = filter_ruble_transactions(filtered_data)

    # Поиск по строке в описании
    search_term = get_search_term()
    if search_term:
        filtered_data = process_bank_search(filtered_data, search_term)

    # Вывод результатов
    print("Распечатываю итоговый список транзакций...")
    if not filtered_data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"\nВсего банковских операций в выборке: {len(filtered_data)}\n")
        for i, operation in enumerate(filtered_data, 1):
            print(f"{i}. {format_operation(operation)}")


if __name__ == "__main__":
    main()
