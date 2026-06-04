# # Вызов фреймворка pytest и функций из generators

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_discriptions


@pytest.fixture
def sample_transaction():
    """Фикстура для подготовки данных"""
    return [
        {"id": 1, "currency": "USD", "amount": 100, "discription": "Покупка в магазине"},
        {"id": 2, "currency": "EUR", "amount": 5600, "discription": "Оплата услуг"},
        {"id": 3, "currency": "RUB", "amount": 5051704, "discription": "Оплата налогов"},
        {"id": 4, "currency": "USD", "amount": 1200, "discription": "Перевод в другой банк"},
        {"id": 5, "currency": "GBP", "amount": 11588866, "discription": "Перевод на вклад"},
    ]


def test_filter_by_currency_usd(sample_transaction):
    """Тест по фильтрации транзакций по USD"""
    usd_filter_transaction = list(filter_by_currency(sample_transaction, currency="USD"))
    assert len(usd_filter_transaction) == 2
    assert usd_filter_transaction[0]["id"] == 1
    assert usd_filter_transaction[1]["id"] == 4


def test_filter_by_curreency_eur(sample_transaction):
    """Тест по фильтрации транзакций по EUR"""
    eur_filter_transaction = list(filter_by_currency(sample_transaction, currency="EUR"))
    assert len(eur_filter_transaction) == 1
    assert eur_filter_transaction[0]["id"] == 2


def test_filter_by_currency_rub(sample_transaction):
    """Тест по фильтрации транзакций по RUB"""
    rub_filter_transaction = list(filter_by_currency(sample_transaction, currency="RUB"))
    assert len(rub_filter_transaction) == 1
    assert rub_filter_transaction[0]["id"] == 3


def test_filter_by_currency_gbp(sample_transaction):
    """Тест по фильтрации транзакций по GPB"""
    gbp_filter_transaction = list(filter_by_currency(sample_transaction, currency="GBP"))
    assert len(gbp_filter_transaction) == 1
    assert gbp_filter_transaction[0]["id"] == 5


def test_filter_by_currency_empty(sample_transaction):
    """Тест фильтрации с отсутствием совпадений."""
    empty_filter_transaction = list(filter_by_currency(sample_transaction, currency="CNY"))
    assert len(empty_filter_transaction) == 0


def test_transaction_descriptions(sample_transaction):
    """Тест генератора описаний транзакций."""
    descriptions = list(transaction_discriptions(sample_transaction))
    expected = ["Покупка в магазине", "Оплата услуг", "Оплата налогов", "Перевод в другой банк", "Перевод на вклад"]
    assert descriptions == expected


def test_card_number_generator_default():
    """Тест генератора карт с параметрами по умолчанию."""
    gener = card_number_generator()
    first_card = next(gener)
    assert first_card == "0000 0000 0000 0001"


def test_card_number_generator_range():
    """Тест генератора карт в заданном диапазоне."""
    gen_ca = card_number_generator(started=9999999999999997, stop=9999999999999999)
    cards = list(gen_ca)
    expected = ["9999 9999 9999 9997", "9999 9999 9999 9998", "9999 9999 9999 9999"]
    assert cards == expected


def test_card_number_generator_single():
    """Тест генератора одной карты."""
    gen = card_number_generator(started=1234567890123456, stop=1234567890123456)
    card = next(gen)
    assert card == "1234 5678 9012 3456"
