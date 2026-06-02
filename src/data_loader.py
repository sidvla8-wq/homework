import csv
import json

import pandas as pd


def load_json_data(file_path: str) -> list[dict]:
    """Загрузка данных из JSON-файла"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv_data(file_path: str) -> list[dict]:
    """Загрузка данных из CSV-файла"""
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_xlsx_data(file_path: str) -> list[dict]:
    """Загрузка данных из XLSX-файла"""
    df = pd.read_excel(file_path)
    return df.to_dict("records")
