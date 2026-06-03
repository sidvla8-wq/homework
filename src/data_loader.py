import csv
import json

import pandas as pd


def read_json(file_path: str) -> list[dict]:
    """Чтение данных из JSON-файла."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_csv(file_path: str) -> list[dict]:
    """Чтение CSV-файла с нестандартным разделителем (;) и структурой."""
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        headers = next(reader)  # Читаем заголовки

        for row in reader:
            if len(row) == len(headers):  # Проверяем, что строка полная
                operation = dict(zip(headers, row))
                data.append(operation)
    return data


def read_excel(file_path: str) -> list[dict]:
    """Чтение данных из XLSX-файла."""
    df = pd.read_excel(file_path)
    return df.to_dict("records")
