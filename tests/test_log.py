# Тестируем модули masks и utils
import pytest
from src.masks import apply_mask
from src.utils import process_data

def test_apply_mask():
    result = apply_mask("4111111111111111")
    assert result == "***1111"

def test_process_data():
    result = process_data("hello world")
    assert result == "HELLO WORLD"

if __name__ == "__main__":
    print("Запуск приложения...")

    # Используем логгер модуля masks
    masked_data = apply_mask("4111111111111111")

    # Используем логгер модуля utils
    processed_data = process_data("hello world")

    print("Приложение завершено.")
