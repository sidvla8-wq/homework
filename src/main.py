from src.bank_operations import (filter_by_status, filter_ruble_transactions, format_date, mask_account_number,
                                 mask_card_number, process_bank_search, sort_by_date)
from src.data_loader import read_csv, read_excel, read_json

FILE_PATHS = {"1": "data/oper.json", "2": "data/transactions.csv", "3": "data/transactions_excel.xlsx"}

VALID_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]


def normalize_user_input(user_input: str) -> bool:
    normalized = user_input.strip().lower()
    return normalized in ("да", "yes", "y", "д")


def get_file_data(choice: str) -> list[dict]:
    file_path = FILE_PATHS[choice]
    if choice == "1":
        return read_json(file_path)
    elif choice == "2":
        return read_csv(file_path)
    else:
        return read_excel(file_path)


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input().strip()
        if choice in FILE_PATHS:
            break
        print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

    print(f"Для обработки выбран {['JSON', 'CSV', 'XLSX'][int(choice)-1]}-файл.")

    try:
        data = get_file_data(choice)
        print(f"Всего операций в файле: {len(data)}")
        if not data:
            print("Файл пуст или не содержит данных.")
            return

        # Диагностика структуры данных
        print("\n--- ДИАГНОСТИКА: структура данных ---")
        print(f"Поля в первой операции: {list(data[0].keys()) if data else 'нет данных'}")
        print(f"Пример первой операции: {data[0] if data else 'нет данных'}")
        print("--- КОНЕЦ ДИАГНОСТИКИ ---\n")

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    # Фильтрация по статусу
    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(VALID_STATUSES)}")
        status = input().strip().upper()
        try:
            filtered_data = filter_by_status(data, status)
            print(f"Операции отфильтрованы по статусу '{status}'. Найдено: {len(filtered_data)} операций")
            break
        except ValueError as e:
            print(e)

    if not filtered_data:
        print("Не найдено ни одной транзакции с указанным статусом.")
        return

    # Сортировка по дате
    print("Отсортировать операции по дате? Да/Нет")
    sort_choice = input()
    if normalize_user_input(sort_choice):
        print("Отсортировать по возрастанию или по убыванию?")
        order_choice = input().strip().lower()
        ascending = "возрастанию" in order_choice or "asc" in order_choice
        filtered_data = sort_by_date(filtered_data, ascending)
        print(f"Операций после сортировки: {len(filtered_data)}")

    if not filtered_data:
        print("После сортировки не осталось транзакций.")
        return

    # Фильтрация рублёвых транзакций
    print("Выводить только рублёвые транзакции? Да/Нет")
    ruble_choice = input()
    if normalize_user_input(ruble_choice):
        filtered_data = filter_ruble_transactions(filtered_data)
        print(f"Операций после фильтрации рублёвых: {len(filtered_data)}")
    if not filtered_data:
        print("После фильтрации по валюте не осталось транзакций.")
        return

    # Поиск по описанию
    print("Отфильтровать список транзакций по определённому слову в описании? Да/Нет")
    search_choice = input()
    if normalize_user_input(search_choice):
        print("Введите слово для поиска:")
        search_term = input().strip()
        if search_term:
            filtered_data = process_bank_search(filtered_data, search_term)
            print(f"Операций после поиска по слову: {len(filtered_data)}")

    if not filtered_data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        # print("Распечатываю итоговый список транзакций...")
        # print(f"Всего банковских операций в выборке: {len(filtered_data)}")
        # for i, operation in enumerate(filtered_data, 1):
        #     # Извлекаем дату
        #     date = operation.get("date", "N/A")
        #
        #     # Извлекаем описание
        #     description = operation.get("description", "N/A")
        #
        #     # Извлекаем сумму — с учётом разных форматов данных
        #     amount = "N/A"
        #
        #     # 1. Для JSON: берём из operationAmount.amount
        #     if "operationAmount" in operation and isinstance(operation["operationAmount"], dict):
        #         amount = operation["operationAmount"].get("amount", "N/A")
        #
        #     # 2. Для CSV: берём из поля amount
        #     elif "amount" in operation:
        #         amount = operation["amount"]
        #
        #     # Извлекаем валюту — с учётом разных форматов данных
        #     currency = "N/A"
        #
        #     # 1. Для JSON: берём из operationAmount.currency.name
        #     if (
        #         "operationAmount" in operation
        #         and isinstance(operation["operationAmount"], dict)
        #         and "currency" in operation["operationAmount"]
        #         and isinstance(operation["operationAmount"]["currency"], dict)
        #     ):
        #         currency = operation["operationAmount"]["currency"].get("name", "N/A")
        #     # 2. Для CSV: берём из currency_name
        #     elif "currency_name" in operation:
        #         currency = operation["currency_name"]
        #     # 3. Для CSV: берём из currency_code
        #     elif "currency_code" in operation:
        #         currency = operation["currency_code"]
        #
        #     print(f"\n{i}. {date} — {description}")
        #     print(f"Сумма: {amount} {currency}")
        print("Распечатываю итоговый список транзакций...")
        print(f"Всего банковских операций в выборке: {len(filtered_data)}")

        for i, operation in enumerate(filtered_data, 1):
            # Преобразуем дату
            date = format_date(operation.get("date", "N/A"))

            # Извлекаем описание
            description = operation.get("description", "N/A")

            # Извлекаем и маскируем «from»
            from_field = operation.get("from", "")
            if from_field:
                if "карта" in from_field.lower() or any(
                    card in from_field for card in ["Visa", "MasterCard", "Maestro"]
                ):
                    from_display = mask_card_number(from_field)
                else:
                    from_display = mask_account_number(from_field)
            else:
                from_display = ""

            # Извлекаем и маскируем «to»
            to_field = operation.get("to", "")
            if to_field:
                if "карта" in to_field.lower() or any(card in to_field for card in ["Visa", "MasterCard", "Maestro"]):
                    to_display = mask_card_number(to_field)
                else:
                    to_display = mask_account_number(to_field)
            else:
                to_display = ""

            # Извлекаем сумму
            amount = "N/A"
            if "operationAmount" in operation and isinstance(operation["operationAmount"], dict):
                amount = operation["operationAmount"].get("amount", "N/A")
            elif "amount" in operation:
                amount = operation["amount"]

            # Извлекаем валюту
            currency = "N/A"
            if (
                "operationAmount" in operation
                and isinstance(operation["operationAmount"], dict)
                and "currency" in operation["operationAmount"]
                and isinstance(operation["operationAmount"]["currency"], dict)
            ):
                currency = operation["operationAmount"]["currency"].get("name", "N/A")
            elif "currency_name" in operation:
                currency = operation["currency_name"]
            elif "currency_code" in operation:
                currency = operation["currency_code"]

            # Форматируем вывод
            print(f"\n{date} {description}")

            # Выводим «from», если есть
            if from_display:
                print(from_display)

            # Если есть и «from», и «to», показываем перевод
            if from_display and to_display:
                print(f"-> {to_display}")
            elif to_display:  # Только «to»
                print(to_display)

            print(f"Сумма: {amount} {currency}")


if __name__ == "__main__":
    main()
