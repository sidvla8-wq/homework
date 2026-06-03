import os

from bank_operations import filter_by_status, filter_ruble_transactions, process_bank_search, sort_by_date
from data_loader import load_csv_data, load_json_data, load_xlsx_data


def get_file_path(file_type: str) -> str:
    """Получение пути к файлу в папке data с проверкой существования"""
    base_path = "data"

    # Создаём папку data, если её нет
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        print(f"Программа: Создана папка '{base_path}' для хранения файлов.")

    max_attempts = 3
    attempt = 0

    while attempt < max_attempts:
        attempt += 1
        filename = input(f"Введите имя {file_type}‑файла (без пути): ").strip()

        # Проверяем, что имя файла не пустое
        if not filename:
            print("Программа: Имя файла не может быть пустым. Попробуйте ещё раз.")
            continue

        # Добавляем расширение, если его нет
        if not filename.lower().endswith(f".{file_type}"):
            filename += f".{file_type}"

        full_path = os.path.join(base_path, filename)

        # Проверяем существование файла
        if os.path.exists(full_path):
            print(f"Программа: Файл найден: {full_path}")
            return full_path
        else:
            remaining = max_attempts - attempt
            if remaining > 0:
                print(f"Программа: Файл '{full_path}' не найден.")
                print(f"Программа: У вас осталось {remaining} попыток.")
                # Показываем содержимое папки для справки
                if os.listdir(base_path):
                    print(f"Программа: Содержимое папки '{base_path}':")
                    for f in os.listdir(base_path):
                        print(f"  - {f}")
                else:
                    print(f"Программа: Папка '{base_path}' пуста.")
            else:
                raise FileNotFoundError(f"Файл '{full_path}' не найден после {max_attempts} попыток.")

    raise FileNotFoundError("Превышено количество попыток ввода имени файла.")


def get_status() -> str:
    """Получение статуса от пользователя с валидацией"""
    allowed_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input(
            "Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n"
            f"Доступные для фильтровки статусы: {', '.join(allowed_statuses)}\n"
        ).strip()
        if status.upper() in allowed_statuses:
            return status.upper()
        print(f"Программа: Статус операции '{status}' недоступен.")


def get_yes_no_input(prompt: str) -> bool:
    """Получение ответа 'да/нет' от пользователя"""

    def get_yes_no_input(prompt: str) -> bool:
        """Получение ответа 'да/нет' от пользователя с обработкой опечаток"""
        yes_variants = ["да", "yes", "y", "д", "lf"]
        no_variants = ["нет", "no", "n", "н", "yz"]

        while True:
            response = input(prompt).strip().lower()
            # Обработка распространённых опечаток
            if "возраст" in response or "asc" in response:
                return True
            elif "убыв" in response or "desc" in response:
                return False

            if response in yes_variants:
                return True
            elif response in no_variants:
                return False
            else:
                print("Пожалуйста, ответьте 'да' или 'нет' (или 'y'/'n').")


def format_transaction(transaction: dict) -> str:
    """Форматирование транзакции для вывода"""
    date = transaction.get("date", "N/A")
    description = transaction.get("description", "N/A")
    account = transaction.get("account", "N/A")
    amount = transaction.get("amount", "N/A")
    return f"{date} {description}\n{account}\nСумма: {amount}\n"


def main():
    """Основная функция программы для работы с банковскими транзакциями."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Цикл для валидации выбора меню
    while True:
        choice = input("Ваш выбор: ").strip()

        if choice in ["1", "2", "3"]:
            break
        else:
            print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")

    transactions = []

    # Загрузка данных в зависимости от выбора пользователя
    try:
        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            file_path = get_file_path("json")
            transactions = load_json_data(file_path)
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            file_path = get_file_path("csv")
            transactions = load_csv_data(file_path)
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            file_path = get_file_path("xlsx")
            transactions = load_xlsx_data(file_path)
    except FileNotFoundError:
        print("Файл не найден. Проверьте путь и имя файла.")
        return
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return

    # Фильтрация по статусу
    status = get_status()
    print(f'Операции отфильтрованы по статусу "{status}"')
    transactions = filter_by_status(transactions, status)

    # Сортировка по дате
    if get_yes_no_input("Программа: Отсортировать операции по дате? Да/Нет\n"):
        while True:
            order = input("Программа: Отсортировать по возрастанию или по убыванию?\n").strip().lower()
            if "возраста" in order:
                ascending = True
                break
            elif "убыва" in order:
                ascending = False
                break
            else:
                print("Программа: Пожалуйста, введите 'по возрастанию' или 'по убыванию'.")
        transactions = sort_by_date(transactions, ascending=ascending)

    # Фильтрация рублёвых транзакций
    if get_yes_no_input("Выводить только рублевые транзакции? Да/Нет\n"):
        transactions = filter_ruble_transactions(transactions)

    # Поиск по описанию
    if get_yes_no_input("Отфильтровать список транзакций по определённому слову в описании? Да/Нет\n"):
        search_term = input("Введите слово для поиска в описании:\n").strip()
        if search_term:
            transactions = process_bank_search(transactions, search_term)

    # Вывод результата
    print("Распечатываю итоговый список транзакций...")

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(transactions)}\n")
        for transaction in transactions:
            formatted = format_transaction(transaction)
            print(formatted)


if __name__ == "__main__":
    main()
