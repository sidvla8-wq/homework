import datetime
import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Поиск транзакций по строке в описании с использованием регулярных выражений"""
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = []
    for transaction in data:
        description = transaction.get("description", "")
        if pattern.search(description):
            result.append(transaction)
    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчёт количества операций по категориям с использованием Counter"""
    # Создаём счётчик для категорий
    category_counter = Counter()

    # Инициализируем счётчик нулями для всех категорий
    for category in categories:
        category_counter[category] = 0

    # Подсчитываем операции по категориям
    for transaction in data:
        description = transaction.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                category_counter[category] += 1

    return dict(category_counter)


def filter_by_status(data: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Фильтрация транзакций по статусу (с приведением к единому регистру)"""
    target_status = status.upper()
    allowed_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    if target_status not in allowed_statuses:
        raise ValueError(f"Статус '{status}' недоступен. Доступные: {', '.join(allowed_statuses)}")
    return [t for t in data if t.get("status", "").upper() == target_status]


def sort_by_date(transactions: list[dict], ascending: bool = True) -> list[dict]:
    """Сортирует транзакции по дате с поддержкой разных форматов."""

    def parse_date(date_str):
        date_formats = ["%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d", "%m/%d/%Y"]
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return datetime.min  # Если формат не распознан

    # Фильтруем транзакции с корректной датой
    valid_transactions = [t for t in transactions if t.get("date")]
    sorted_transactions = sorted(valid_transactions, key=lambda x: parse_date(x["date"]), reverse=not ascending)
    return sorted_transactions


def filter_ruble_transactions(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрация только рублёвых транзакций"""
    ruble_currencies = ["руб.", "рубль", "rub"]
    result = []
    for transaction in data:
        amount_str = str(transaction.get("amount", ""))
        if any(currency in amount_str.lower() for currency in ruble_currencies):
            result.append(transaction)
    return result
