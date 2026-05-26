import json
import os
from typing import Dict, List

from src.logging_config import utils_logger


# Создаём логгер для модуля utils
def validate_input(value):
    utils_logger.debug(f"Проверка входных данных: {value}")
    if not value:
        utils_logger.warning("Получены пустые входные данные")
        return False
    if len(str(value)) < 3:
        utils_logger.warning(f"Данные слишком короткие: {value}")
        return False
    utils_logger.info("Входные данные прошли валидацию")
    return True


def process_data(data):
    try:
        utils_logger.info(f"Начинаем обработку данных: {data}")
        if validate_input(data):
            result = data.upper()
            utils_logger.info(f"Обработка завершена успешно. Результат: {result}")
            return result
        else:
            utils_logger.error("Валидация данных не пройдена")
            return None
    except Exception as e:
        utils_logger.error(f"Ошибка при обработке данных: {e}")
        raise


# Пример использования
if __name__ == "__main__":
    process_data("test data")


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
