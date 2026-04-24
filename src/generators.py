# Делаю задание связанное с генераторами транзакций


def filter_by_currency(transactions: list(dict), currency: str) -> iter:
    """Функция для возвращения итератора, который поочередно выдает транзакции,
    где валюта операции соответствует заданной (например, USD)"""
    for transaction in transactions:
        if transaction["currency"] == currency:
            yield transaction


def transaction_discriptions(transactions: list(dict)) -> iter:
    """Генератор транзакций, возвращающий описание каждой операции по очереди"""
    for transaction in transactions:
        yield transaction.get("discription", "")


def card_number_generator(started: int = 1, stop: int = 9999999999999999) -> iter:
    """Генератор , который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где X — цифра номера карты."""
    for num in range(started, stop + 1):
        card_str = f"{num:016d}"
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        yield formatted_card
