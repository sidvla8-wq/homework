import os
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.exchangeratesapi.io/latest"
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")


def get_exchange_rate(base_currency: str, target_currency: str = "RUB") -> Optional[float]:
    """Получает актуальный курс валюты через API"""
    try:
        params = {"access_key": API_KEY, "base": base_currency, "symbols": target_currency}
        response = requests.get(API_URL, params=params)
        response.raise_for_status()

        data = response.json()
        return data["rates"][target_currency]
    except (requests.RequestException, KeyError):
        return None


def convert_to_rubles(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли"""
    amount = float(transaction.get("amount", 0))
    currency = transaction.get("currency", "RUB")

    if currency == "RUB":
        return amount

    rate = get_exchange_rate(currency)
    if rate is not None:
        return amount * rate
    else:
        raise ValueError(f"Не удалось получить курс для валюты {currency}")
