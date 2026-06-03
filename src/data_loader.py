import csv
import json
import re

import pandas as pd


def fix_json_file(input_path: str, output_path: str = None):
    """
    Пытается автоматически исправить распространённые ошибки в JSON‑файле.
    """
    if output_path is None:
        output_path = input_path

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Замена одинарных кавычек на двойные (осторожно: может нарушить строки)
    content = re.sub(r"'([^'\"]*)'", r'"\1"', content)

    # Экранирование кавычек внутри строковых значений
    content = re.sub(r'(?<!\\)"', r"\"", content)

    # Удаление комментариев //
    content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)

    # Удаление комментариев /* */
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    try:
        data = json.loads(content)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Файл успешно исправлен и сохранён как {output_path}")
        return True
    except json.JSONDecodeError as e:
        print(f"Не удалось автоматически исправить файл: {e}")
        return False


def load_json_data(file_path: str) -> list[dict]:
    """Загрузка данных из JSON-файла"""
    # with open(file_path, "r", encoding="utf-8") as f:
    #     return json.load(f)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Базовая проверка на пустой файл
        if not content.strip():
            raise ValueError("Файл пуст")

        data = json.loads(content)

        # Проверяем, что данные — список словарей
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    raise ValueError("Элементы в JSON должны быть словарями")
        elif isinstance(data, dict):
            # Если JSON — один словарь, оборачиваем в список
            data = [data]
        else:
            raise ValueError("JSON должен содержать список или словарь")

        return data

    except json.JSONDecodeError as e:
        print(f"Программа: Ошибка синтаксиса JSON в файле {file_path}")
        print(f"Программа: Детальная ошибка: {e}")
        print(f"Программа: Проблема в строке {e.lineno}, позиция {e.colno}")

        # Показываем проблемный участок (50 символов до и после ошибки)
        start = max(0, e.pos - 50)
        end = e.pos + 50
        context = content[start:end]
        print(f"Программа: Контекст ошибки:\n{context}")

        raise ValueError(f"Некорректный JSON: {e}")

    except UnicodeDecodeError:
        raise ValueError("Ошибка кодировки файла. Убедитесь, что файл сохранён в UTF-8.")
    except Exception as e:
        raise ValueError(f"Неожиданная ошибка при чтении файла: {e}")


def load_csv_data(file_path: str) -> list[dict]:
    """Загрузка данных из CSV-файла"""
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_xlsx_data(file_path: str) -> list[dict]:
    """Загрузка данных из XLSX-файла"""
    df = pd.read_excel(file_path)
    return df.to_dict("records")
