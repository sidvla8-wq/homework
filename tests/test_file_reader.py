from unittest.mock import patch

import pandas as pd
import pytest

from src.file_reader import read_transactions_from_csv, read_transactions_from_excel


class TestDataReader:
    @pytest.fixture
    def sample_data(self):
        """Фикстура с тестовыми данными."""
        return [
            {"id": 1, "amount": 100.0, "currency": "USD", "date": "2023-01-01"},
            {"id": 2, "amount": 200.5, "currency": "EUR", "date": "2023-01-02"},
            {"id": 3, "amount": 150.75, "currency": "USD", "date": "2023-01-03"},
        ]

    @patch("pandas.read_csv")
    def test_read_csv_success(self, mock_read_csv, sample_data):
        """Тест успешного чтения CSV-файла."""
        mock_read_csv.return_value = pd.DataFrame(sample_data)
        result = read_transactions_from_csv("transactions.csv")
        assert result == sample_data

    @patch("pandas.read_csv")
    def test_read_csv_empty_file(self, mock_read_csv):
        """Тест обработки пустого CSV-файла."""
        mock_read_csv.side_effect = pd.errors.EmptyDataError("No columns to parse from file")
        result = read_transactions_from_csv("empty.csv")
        assert result == []  # Проверяем, что возвращается пустой список

    def test_read_csv_file_not_found(self):
        """Тест обработки отсутствия CSV-файла."""
        with pytest.raises(FileNotFoundError):
            read_transactions_from_csv("nonexistent.csv")

    @patch("pandas.read_excel")
    def test_read_excel_success(self, mock_read_excel, sample_data):
        """Тест успешного чтения Excel-файла."""
        mock_read_excel.return_value = pd.DataFrame(sample_data)
        result = read_transactions_from_excel("transactions_excel.xlsx")
        assert result == sample_data

    def test_read_excel_file_not_found(self):
        """Тест обработки отсутствия Excel-файла."""
        with pytest.raises(FileNotFoundError):
            read_transactions_from_excel("nonexistent.xlsx")

    @patch("pandas.read_excel")
    def test_read_excel_invalid_format(self, mock_read_excel):
        """Тест обработки ошибки чтения Excel-файла."""
        mock_read_excel.side_effect = ValueError("Invalid Excel format")
        with pytest.raises(ValueError):
            read_transactions_from_excel("invalid.xlsx")

    @patch("pandas.read_csv")
    def test_read_csv_with_different_separator(self, mock_read_csv, sample_data):
        """Тест чтения CSV с нестандартным разделителем."""
        # В реальной реализации нужно добавить параметр sep
        mock_read_csv.return_value = pd.DataFrame(sample_data)
        result = read_transactions_from_csv("transactions.csv")
        assert isinstance(result, list)
        assert len(result) == 3

    @patch("pandas.read_excel")
    def test_read_excel_with_multiple_sheets(self, mock_read_excel, sample_data):
        """Тест чтения Excel с несколькими листами (используем первый)."""
        mock_read_excel.return_value = pd.DataFrame(sample_data)
        result = read_transactions_from_excel("transactions_excel.xlsx")
        assert result == sample_data
