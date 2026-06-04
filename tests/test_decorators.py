# Тестирую модуль decorators

import os

import pytest

from src.decorators import log


# Вспомогательная функция для очистки лог‑файла
def cleanup_log_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


class TestLogDecorator:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Очищаем тестовые файлы до и после тестов"""
        cleanup_log_file("test_log.txt")
        yield
        cleanup_log_file("test_log.txt")

    def test_successful_function_execution_with_file(self):
        """Тест: успешное выполнение функции с логированием в файл"""

        @log("test_log.txt")
        def sample_function(x, y):
            return x + y

        result = sample_function(5, 3)

        assert result == 8

        # Проверяем содержимое лог‑файла
        with open("test_log.txt", "r", encoding="utf-8") as f:
            content = f.read()

        assert "sample_function ok" in content

    def test_successful_function_execution_without_file(self, capsys):
        """Тест: успешное выполнение функции с логированием в консоль"""

        @log()
        def another_function():
            return "Hello"

        result = another_function()

        assert result == "Hello"

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "another_function ok" in captured.out

    def test_function_with_exception_with_file(self):
        """Тест: функция вызывает исключение с логированием в файл"""

        @log("test_log.txt")
        def faulty_function():
            raise ValueError("Something went wrong")

        with pytest.raises(ValueError, match="Something went wrong"):
            faulty_function()

        # Проверяем лог‑файл
        with open("test_log.txt", "r", encoding="utf-8") as f:
            content = f.read()

        assert "faulty_function ошибка: ValueError" in content
        assert "Входные данные: (), {}" in content

    def test_function_with_exception_without_file(self, capsys):
        """Тест: функция вызывает исключение с логированием в консоль"""

        @log()
        def problematic_function(a, b):
            return a / b

        with pytest.raises(ZeroDivisionError):
            problematic_function(10, 0)

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "problematic_function ошибка: ZeroDivisionError" in captured.out
        assert "Входные данные: (10, 0), {}" in captured.out

    def test_function_with_arguments(self, capsys):
        """Тест: функция с аргументами и kwargs"""

        @log()
        def complex_function(name, age, city="Moscow"):
            return f"{name} {age} лет и она живет в городе {city}"

        result = complex_function("Карина", 25, city="Москва")

        assert result == "Карина 25 лет и она живет в городе Москва"

        # Проверяем логирование аргументов
        captured = capsys.readouterr()
        assert "complex_function ok" in captured.out
        # В логе должны быть аргументы, но в текущем декораторе они логируются только при ошибке

    def test_multiple_function_calls(self):
        """Тест: многократный вызов функции с логированием в один файл"""

        @log("test_log.txt")
        def counter_function(n):
            return n * 2

        counter_function(1)
        counter_function(2)
        counter_function(3)

        # Проверяем, что все вызовы записаны в файл
        with open("test_log.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 3
        assert all("counter_function ok" in line for line in lines)

    def test_empty_filename_parameter(self, capsys):
        """Тест: явное указание None в качестве filename"""

        @log(None)
        def simple_function():
            return True

        result = simple_function()
        assert result is True

        captured = capsys.readouterr()
        assert "simple_function ok" in captured.out

    def test_file_encoding(self):
        """Тест: проверка кодировки UTF‑8 при записи в файл"""

        @log("test_log.txt")
        def unicode_function():
            return "Привет"

        unicode_function()

        # Проверяем, что файл записан с правильной кодировкой
        with open("test_log.txt", "r", encoding="utf-8") as f:
            content = f.read()

        assert "unicode_function ok" in content
