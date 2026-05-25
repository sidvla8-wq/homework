import json
import os
from typing import Dict, List
# from log_config import setup_logger
#
# # Создаём логгер для модуля utils
# logger = setup_logger(__name__, 'utils.log')
#
# # Пример использования логгера
# def load_transactions(operations: str):
#     logger.info(f"Загружаем транзакции из файла: {operations}")
#     try:
#         # Логика загрузки транзакций
#         data = []  # Замените на реальную логику
#         logger.debug(f"Данные успешно загружены: {len(data)} записей")
#         return data
#     except FileNotFoundError as e:
#         logger.error(f"Файл не найден: {operations}")
#         raise
#     except json.JSONDecodeError as e:
#         logger.error(f"Ошибка парсинга JSON в файле {operations}: {e}")
#         raise
#     except Exception as e:
#         logger.critical(f"Критическая ошибка при загрузке транзакций: {e}")
#         raise


def load_transactions(operations: str) -> List[Dict]:
    """Загружает данные о финансовых транзакциях из JSON-файла"""
    # Проверяем существование файла
    if not os.path.exists(operations):
        raise FileNotFoundError(f"Файл {operations} не найден")

    try:
        with open(operations, "r", encoding="utf-8") as f:
            data = json.load(f)  # Корректный вызов json.load()

        # Проверяем, что данные — список
        if isinstance(data, list):
            return data
        else:
            raise ValueError(f"Данные в файле {operations} не являются списком")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON в файле {operations}: {e}")
