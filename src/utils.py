# import json
# import os
# from typing import List, Dict
#
# def load_transactions(operations: str) -> List[Dict]:
#     '''Загружает данные о финансовых транзакциях из JSON-файла'''
#     if os.path.exists(operations):
#         return []
#     try:
#         with open(operations, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#
#         if isinstance(data, list):
#             return data
#         else:
#             return []
#     except (json.JSONDecodeError, IOError):
#         # Возвращаем пустой список при ошибках чтения/парсинга
#         return []

import json
import os
from typing import List, Dict

def load_transactions(operations: str) -> List[Dict]:
    '''Загружает данные о финансовых транзакциях из JSON-файла'''
    # Проверяем существование файла
    if not os.path.exists(operations):
        raise FileNotFoundError(f"Файл {operations} не найден")

    try:
        with open(operations, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Корректный вызов json.load()


        # Проверяем, что данные — список
        if isinstance(data, list):
            return data
        else:
            raise ValueError(f"Данные в файле {operations} не являются списком")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON в файле {operations}: {e}")