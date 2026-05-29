import json
from unittest.mock import mock_open, patch

import pytest

from src.external_api import convert_to_rubles
from src.utils import load_transactions


@patch("builtins.open", mock_open(read_data='[{"id": 1, "amount": 100}]'))
def test_load_transactions_success():
    pass


@patch("os.path.exists", return_value=False)
def test_load_transactions_file_not_found(mock_exists):
    with pytest.raises(FileNotFoundError) as exc_info:
        result = load_transactions("nonexistent.json")
        return result

    # Проверяем сообщение об ошибке дополнительно
    assert "nonexistent.json" in str(exc_info.value)


def test_load_transactions_invalid_json():
    with patch("builtins.open", mock_open(read_data="not a list")) as mock_open_patch, patch(
        "json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0)
    ) as mock_json_patch, patch("os.path.exists", return_value=True) as mock_exists:

        with pytest.raises(ValueError) as exc_info:
            load_transactions("invalid.json")

        # Проверяем сообщение об ошибке — оно должно содержать исходное сообщение JSONDecodeError
        assert "Ошибка парсинга JSON" in str(exc_info.value)
        assert "Expecting value" in str(exc_info.value)

        # Проверяем вызовы моков
        mock_open_patch.assert_called_once_with("invalid.json", "r", encoding="utf-8")
        mock_json_patch.assert_called_once()
        mock_exists.assert_called_once_with("invalid.json")


def test_load_transactions_not_a_list(monkeypatch):
    # Мокируем os.path.exists — файл существует
    monkeypatch.setattr("os.path.exists", lambda x: True)

    # Мокируем builtins.open
    mock_file = mock_open(read_data='"not a list"')
    monkeypatch.setattr("builtins.open", mock_file)

    with pytest.raises(ValueError) as exc_info:
        load_transactions("not_a_list.json")

    assert "Данные в файле not_a_list.json не являются списком" in str(exc_info.value)
    mock_file.assert_called_once_with("not_a_list.json", "r", encoding="utf-8")


@patch("src.external_api.get_exchange_rate", return_value=75.0)
def test_convert_to_rubles_usd(mock_get_rate):
    transaction = {"amount": 10, "currency": "USD"}
    result = convert_to_rubles(transaction)
    assert pytest.approx(result, 0.01) == 750.0


@patch("src.external_api.get_exchange_rate", return_value=85.0)
def test_convert_to_rubles_eur(mock_get_rate):
    transaction = {"amount": 20, "currency": "EUR"}
    result = convert_to_rubles(transaction)
    assert pytest.approx(result, 0.01) == 1700.0


def test_convert_to_rubles_rub():
    transaction = {"amount": 1000, "currency": "RUB"}
    result = convert_to_rubles(transaction)
    assert result == 1000.0


@patch("src.external_api.get_exchange_rate", return_value=None)
def test_convert_to_rubles_no_rate(mock_get_rate):
    transaction = {"amount": 10, "currency": "USD"}
    with pytest.raises(ValueError, match="Не удалось получить курс для валюты USD"):
        convert_to_rubles(transaction)
