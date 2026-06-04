from typing import Dict, List

import pandas as pd


def read_transactions_from_csv(file_path: str) -> List[Dict]:  # file_path (str): путь к CSV-файлу.
    """Считываем финансовые операции из CSV-файла"""
    try:
        df = pd.read_csv(file_path, sep=",", encoding="utf-8")
        return df.to_dict("records")
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден!")
    except pd.errors.EmptyDataError:
        print("Предупреждение: файл пуст.")
        return []
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Ошибка парсинга CSV: {e}")


def read_transactions_from_excel(file_path: str) -> List[Dict]:
    """Считываем финансовые операции из Excel-файла"""
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        return df.to_dict("records")
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    except ValueError as e:
        raise ValueError(f"Ошибка чтения Excel-файла: {e}")
