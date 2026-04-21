# Вызов фреймворка pytest и функций из masks
import pytest
from src.masks import get_mask_card_number, get_mask_account

@pytest.fixture
def card_number():
    return "9874561230987456"

@pytest.fixture
def account_number():
    return "96385274101234567890"

# Тесты для маскировки номера карты
@pytest.mark.parametrize("card_number,expected", [
    ("9874561230987456", "9874 56** ****7456"),
    ("987456123098745", "Номер карты не содержит 16 цифр"),
    ("98745612309874566", "Номер карты не содержит 16 цифр"),
    ("9874561230987456f", "Номер карты должен состоять из цифр!"),
    ("987456123098-", "Номер карты должен состоять из цифр!"),
    ("9874 5612 3098 7456", "9874 56** ****7456"),
    ("", "Номер карты должен состоять из цифр!")
])
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected

# Тесты для маскировки номера счёта
@pytest.mark.parametrize("account_number,expected", [
    ("96385274101234567890", "**7890"),
    ("9638527410", "Счёт не равен 20 цифрам"),
    ("963852741012345678901", "Счёт не равен 20 цифрам"),
    ("9638527410f", "Счёт должен состоять из цифр!"),
    ("963 527 4101234 567890", "Счёт не равен 20 цифрам"),
    ("", "Счёт должен состоять из цифр!")
])
def test_get_mask_account(account_number, expected):
    assert get_mask_account(account_number) == expected