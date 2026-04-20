# Вызываю стандартную функцию для конвертирования даты согласно заданию.

from datetime import datetime


def filter_by_state(filt_operation: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует список словарей по state"""
    if not isinstance(filt_operation, list):
        raise TypeError("filt_operation должен быть списком")
    filter_data = [item for item in filt_operation if isinstance(item, dict) and item.get("state") == state]
    return filter_data


def sort_by_date(filt_operation: list[dict], reverse: bool = True) -> list[dict]:
    """Функция сортировки по дате"""

    if not isinstance(filt_operation, list):
        raise TypeError("должен быть списком")

    def parse_date(date_str):
        """Парсит строку даты в объект datetime. Поддерживает несколько форматов."""
        formats = [
            "%Y-%m-%dT%H:%M:%S",  # ISO формат: 2023-01-01T10:00:00
            "%Y-%m-%d %H:%M:%S",  # Пробел вместо T: 2023-01-01 10:00:00
            "%Y-%m-%d",  # Только дата: 2023-01-01
        ]
        for frmt in formats:
            try:
                return datetime.strptime(date_str, frmt)
            except ValueError:
                continue
        raise ValueError(f"Не удалось распознать формат даты: {date_str}")

    # Фильтруем элементы, у которых есть ключ 'date' и он не пустой
    it_va = [i for i in filt_operation if isinstance(i, dict) and "date" in i and i["date"]]

    sort_data = sorted(it_va, key=lambda x: parse_date(x["date"]), reverse=reverse)
    return sort_data
