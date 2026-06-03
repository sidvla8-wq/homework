import re
from collections import Counter
from datetime import datetime


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [op for op in data if pattern.search(op.get("description", ""))]


def filter_by_status(data: list[dict], status: str) -> list[dict]:
    status = status.upper()
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    if status not in valid_statuses:
        raise ValueError(f"Статус операции '{status}' недоступен.")

    result = []
    for operation in data:
        status_fields = ["status", "state", "Status", "State", "STATUS", "STATE"]
        for field in status_fields:
            if field in operation and str(operation[field]).upper() == status:
                result.append(operation)
                break
    return result


def parse_date(date_str) -> datetime:
    """Парсинг даты с поддержкой разных форматов."""
    if not date_str:
        return datetime.min
    formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%d.%m.%Y", "%Y-%m-%d"]
    for fmt in formats:
        try:
            return datetime.strptime(str(date_str), fmt)
        except (ValueError, TypeError):
            continue
    return datetime.min


def sort_by_date(data: list[dict], ascending: bool = True) -> list[dict]:
    """Сортировка операций по дате."""

    def get_date_key(operation: dict) -> datetime:
        return parse_date(operation.get("date", ""))

    return sorted(data, key=get_date_key, reverse=not ascending)


# def filter_ruble_transactions(data: list[dict]) -> list[dict]:
#     """Фильтрация рублёвых транзакций с учётом сложной структуры данных."""
#     ruble_indicators = ["руб", "rub", "rur", "₽"]
#     result = []
#
#     for op in data:
#         currency_found = False
#
#         if "operationAmount" in op and isinstance(op["operationAmount"], dict):
#             currency_info = op["operationAmount"].get("currency", {})
#             if isinstance(currency_info, dict):
#                 currency_name = currency_info.get("name", "").lower()
#                 if any(indicator in currency_name for indicator in ruble_indicators):
#                     currency_found = True
#
#         if not currency_found and "amount" in op:
#             amount_str = str(op["amount"]).lower()
#             if any(indicator in amount_str for indicator in ruble_indicators):
#                 currency_found = True
#
#         if not currency_found and "description" in op:
#             desc_str = str(op["description"]).lower()
#             if any(indicator in desc_str for indicator in ruble_indicators):
#                 currency_found = True
#
#         if currency_found:
#             result.append(op)
#     return result


def filter_ruble_transactions(data: list[dict]) -> list[dict]:
    """Фильтрация рублёвых транзакций с учётом разных форматов данных."""
    ruble_indicators = ["руб", "rub", "rur", "₽"]
    ruble_currency_codes = ["RUB"]  # Коды валют для рубля
    result = []

    for op in data:
        currency_found = False

        # 1. Проверяем поле currency_name (для CSV)
        if "currency_name" in op:
            currency_name = str(op["currency_name"]).lower()
            if any(indicator in currency_name for indicator in ruble_indicators):
                currency_found = True

        # 2. Проверяем currency_code (для CSV) — ищем RUB
        if not currency_found and "currency_code" in op:
            currency_code = str(op["currency_code"]).upper()
            if currency_code in ruble_currency_codes:
                currency_found = True

        # 3. Для JSON-структуры: проверяем operationAmount.currency.name
        if not currency_found and "operationAmount" in op and isinstance(op["operationAmount"], dict):
            currency_info = op["operationAmount"].get("currency", {})
            if isinstance(currency_info, dict):
                currency_name = currency_info.get("name", "").lower()
                if any(indicator in currency_name for indicator in ruble_indicators):
                    currency_found = True

        # 4. Проверяем поле amount (если есть)
        if not currency_found and "amount" in op:
            amount_str = str(op["amount"]).lower()
            if any(indicator in amount_str for indicator in ruble_indicators):
                currency_found = True

        # 5. Проверяем описание
        if not currency_found and "description" in op:
            desc_str = str(op["description"]).lower()
            if any(indicator in desc_str for indicator in ruble_indicators):
                currency_found = True

        if currency_found:
            result.append(op)

    return result


def analyze_operations(data: list[dict]) -> dict:
    """
    Анализ операций: подсчёт по статусам, валютам и категориям.
    Использует Counter для эффективной агрегации данных.
    """
    # Подсчёт по статусам
    statuses = [op.get("state") or op.get("status") for op in data]
    status_counts = Counter(statuses)

    # Подсчёт по валютам
    currencies = []
    for op in data:
        if "operationAmount" in op and isinstance(op["operationAmount"], dict):
            currency_info = op["operationAmount"].get("currency", {})
            if isinstance(currency_info, dict):
                currencies.append(currency_info.get("name", "N/A"))
        else:
            currencies.append("N/A")
    currency_counts = Counter(currencies)

    # Подсчёт по описаниям (топ-5 самых частых)
    descriptions = [op.get("description", "N/A").lower() for op in data]
    description_counts = Counter(descriptions).most_common(5)

    return {
        "status_distribution": dict(status_counts),
        "currency_distribution": dict(currency_counts),
        "top_descriptions": description_counts,
    }
