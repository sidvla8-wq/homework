# # # import datetime
# # # import re
# # # from collections import Counter
# # # from typing import Any, Dict, List
# # #
# # #
# # # def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
# # #     """Поиск транзакций по строке в описании с использованием регулярных выражений"""
# # #     pattern = re.compile(re.escape(search), re.IGNORECASE)
# # #     result = []
# # #     for transaction in data:
# # #         description = transaction.get("description", "")
# # #         if pattern.search(description):
# # #             result.append(transaction)
# # #     return result
# # #
# # #
# # # def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
# # #     """Подсчёт количества операций по категориям с использованием Counter"""
# # #     # Создаём счётчик для категорий
# # #     category_counter = Counter()
# # #
# # #     # Инициализируем счётчик нулями для всех категорий
# # #     for category in categories:
# # #         category_counter[category] = 0
# # #
# # #     # Подсчитываем операции по категориям
# # #     for transaction in data:
# # #         description = transaction.get("description", "").lower()
# # #         for category in categories:
# # #             if category.lower() in description:
# # #                 category_counter[category] += 1
# # #
# # #     return dict(category_counter)
# # #
# # #
# # # def filter_by_status(data: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
# # #     """Фильтрация транзакций по статусу (с приведением к единому регистру)"""
# # #     target_status = status.upper()
# # #     allowed_statuses = {"EXECUTED", "CANCELED", "PENDING"}
# # #     if target_status not in allowed_statuses:
# # #         raise ValueError(f"Статус '{status}' недоступен. Доступные: {', '.join(allowed_statuses)}")
# # #     return [t for t in data if t.get("status", "").upper() == target_status]
# # #
# # #
# # # def sort_by_date(transactions: list[dict], ascending: bool = True) -> list[dict]:
# # #     """Сортирует транзакции по дате с поддержкой разных форматов."""
# # #
# # #     def parse_date(date_str):
# # #         date_formats = ["%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d", "%m/%d/%Y"]
# # #         for fmt in date_formats:
# # #             try:
# # #                 return datetime.strptime(date_str, fmt)
# # #             except ValueError:
# # #                 continue
# # #         return datetime.min  # Если формат не распознан
# # #
# # #     # Фильтруем транзакции с корректной датой
# # #     valid_transactions = [t for t in transactions if t.get("date")]
# # #     sorted_transactions = sorted(valid_transactions, key=lambda x: parse_date(x["date"]), reverse=not ascending)
# # #     return sorted_transactions
# # #
# # #
# # # def filter_ruble_transactions(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
# # #     """Фильтрация только рублёвых транзакций"""
# # #     ruble_currencies = ["руб.", "рубль", "rub"]
# # #     result = []
# # #     for transaction in data:
# # #         amount_str = str(transaction.get("amount", ""))
# # #         if any(currency in amount_str.lower() for currency in ruble_currencies):
# # #             result.append(transaction)
# # #     return result
# import re
# from datetime import datetime
# from collections import Counter
#
# def process_bank_search(data: list[dict], search: str) -> list[dict]:
#     """
#     Поиск операций по строке в описании с использованием регулярных выражений.
#
#     Args:
#         data: список словарей с данными о банковских операциях
#         search: строка поиска
#
#     Returns:
#         Список словарей, содержащих строку поиска в описании
#     """
#     pattern = re.compile(re.escape(search), re.IGNORECASE)
#     result = []
#     for operation in data:
#         description = operation.get('description', '')
#         if pattern.search(description):
#             result.append(operation)
#     return result
#
# def process_bank_operations(data: list[dict], categories: list) -> dict:
#     """
#     Подсчёт количества операций по категориям с использованием Counter.
#
#     Args:
#         data: список словарей с данными о банковских операциях
#         categories: список категорий для подсчёта
#
#     Returns:
#         Словарь с количеством операций по каждой категории
#     """
#     # Создаём список категорий, которые встречаются в операциях
#     matched_categories = []
#
#     for operation in data:
#         description = operation.get('description', '').lower()
#         # Проверяем, относится ли операция к какой‑либо из заданных категорий
#         for category in categories:
#             if category.lower() in description:
#                 matched_categories.append(category)
#                 break  # Чтобы не засчитывать операцию в несколько категорий одновременно
#
#     # Используем Counter для подсчёта количества операций по каждой категории
#     category_counter = Counter(matched_categories)
#
#     # Гарантируем, что все заданные категории присутствуют в результате (даже если их счёт — 0)
#     result = {category: category_counter.get(category, 0) for category in categories}
#     return result
#
# def filter_by_status(data: list[dict], status: str) -> list[dict]:
#     """Фильтрация операций по статусу (с приведением к единому регистру)."""
#     status = status.upper()
#     valid_statuses = {'EXECUTED', 'CANCELED', 'PENDING'}
#     if status not in valid_statuses:
#         raise ValueError(f"Статус операции '{status}' недоступен.")
#     return [op for op in data if op.get('state', '').upper() == status]
#
#
# def sort_by_date(data: list[dict], ascending: bool = True) -> list[dict]:
#     """Сортировка операций по дате."""
#     def parse_date(date_str):
#         try:
#             return datetime.strptime(date_str, '%d.%m.%Y')
#         except ValueError:
#             return datetime.min
#     return sorted(data, key=lambda x: parse_date(x.get('date', '')), reverse=not ascending)
#
# def filter_ruble_transactions(data: list[dict]) -> list[dict]:
#     """Фильтрация только рублёвых транзакций."""
#     return [
#         op for op in data
#         if 'руб' in op.get('amount', '').lower() or 'rub' in op.get('currency', '').lower()
#     ]

import re
from datetime import datetime
from collections import Counter

def process_bank_search(data: list[dict], search: str) -> list[dict]:
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [op for op in data if pattern.search(op.get('description', ''))]


def filter_by_status(data: list[dict], status: str) -> list[dict]:
    status = status.upper()
    valid_statuses = {'EXECUTED', 'CANCELED', 'PENDING'}
    if status not in valid_statuses:
        raise ValueError(f"Статус операции '{status}' недоступен.")

    result = []
    for operation in data:
        # Проверяем разные варианты названий поля статуса
        status_fields = ['status', 'state', 'Status', 'State', 'STATUS', 'STATE']
        for field in status_fields:
            if field in operation and str(operation[field]).upper() == status:
                result.append(operation)
                break
    return result

def sort_by_date(data: list[dict], ascending: bool = True) -> list[dict]:
    def parse_date(date_str):
        if not date_str:
            return datetime.min
        # Разные форматы дат
        formats = ['%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']
        for fmt in formats:
            try:
                return datetime.strptime(str(date_str), fmt)
            except (ValueError, TypeError):
                continue
        return datetime.min  # Если формат не распознан

    # Проверяем наличие поля date в данных
    date_fields = ['date', 'Date', 'DATE', 'transaction_date']
    key_func = lambda x: parse_date(
        x.get(date_fields[0],
        x.get(date_fields[1],
        x.get(date_fields[2],
        x.get(date_fields[3], ''))))
    )

    return sorted(data, key=key_func, reverse=not ascending)

def filter_ruble_transactions(data: list[dict]) -> list[dict]:
    """Фильтрация рублёвых транзакций с учётом сложной структуры данных."""
    ruble_indicators = ['руб', 'rub', 'rur', '₽']
    result = []

    for op in data:
        # Проверяем разные возможные места указания валюты
        currency_found = False

        # 1. Проверяем поле operationAmount.currency.name
        if 'operationAmount' in op and isinstance(op['operationAmount'], dict):
            currency_info = op['operationAmount'].get('currency', {})
            if isinstance(currency_info, dict):
                currency_name = currency_info.get('name', '').lower()
                if any(indicator in currency_name for indicator in ruble_indicators):
                    currency_found = True

        # 2. Проверяем поле amount (если есть)
        if not currency_found and 'amount' in op:
            amount_str = str(op['amount']).lower()
            if any(indicator in amount_str for indicator in ruble_indicators):
                currency_found = True

        # 3. Проверяем описание
        if not currency_found and 'description' in op:
            desc_str = str(op['description']).lower()
            if any(indicator in desc_str for indicator in ruble_indicators):
                currency_found = True

        if currency_found:
            result.append(op)

    return result
