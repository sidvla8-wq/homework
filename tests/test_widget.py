# Вызов фреймворка pytest и функций из widget

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** ****6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** ****6361"),
        ("Счёт 73654108430135874305", "Счёт **4305"),
        ("", "Введена пустая строка"),
    ],
)
def test_mask_account_card(input_str, expected):
    assert mask_account_card(input_str) == expected


def test_get_date():
    input_date = "2024-03-11T02:26:18.671407"
    expected = "11.03.2024"
    assert get_date(input_date) == expected
    with pytest.raises(ValueError):
        get_date("Некорректный формат даты")
