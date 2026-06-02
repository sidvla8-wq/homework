import re
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
    """Подсчёт количества операций по категориям"""
    category_counts = {category: 0 for category in categories}
    for transaction in data:
        description = transaction.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                category_counts[category] += 1
    return category_counts


def filter_by_status(data: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Фильтрация транзакций по статусу (с приведением к единому регистру)"""
    target_status = status.upper()
    allowed_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    if target_status not in allowed_statuses:
        raise ValueError(f"Статус '{status}' недоступен. Доступные: {', '.join(allowed_statuses)}")
    return [t for t in data if t.get("status", "").upper() == target_status]


def sort_by_date(data: List[Dict[str, Any]], ascending: bool = True) -> List[Dict[str, Any]]:
    """Сортировка транзакций по дате"""
    return sorted(data, key=lambda x: x.get("date", ""), reverse=not ascending)


def filter_ruble_transactions(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрация только рублёвых транзакций"""
    ruble_currencies = ["руб.", "рубль", "rub"]
    result = []
    for transaction in data:
        amount_str = str(transaction.get("amount", ""))
        if any(currency in amount_str.lower() for currency in ruble_currencies):
            result.append(transaction)
    return result
