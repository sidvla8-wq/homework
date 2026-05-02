# Вызываю стандартный модуль typing, который поддерживает подсказки типов
# Any - когда тип переменной который может быть любым
# Callable - тип обозначающий вызванную функции
# Optional - показывает что переменная и тип могуут быть заданного типа или None

from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования начала и конца выполнения функции,
    а также результатов или ошибок."""

    def decorator(func: Callable) -> Callable:
        """Вызываю функцию которую нужно декорировать"""

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Вызов исходной функции, добавляю логирование"""
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        # Если filename задан то записывает в конец файла благодаря ключу 'a'
                        f.write(f"{message}\n")

                else:
                    print(message)  # Если filename не задан то выводит сообщение

                return result
            except Exception as e:
                errors_func_type = type(e).__name__  # Определяет тип ошибки
                inp_message = f"Входные данные: {args}, {kwargs}"  # Формирует строку с входными данными
                message = f"{func.__name__} ошибка: {errors_func_type}, {inp_message}"  # Сообщение об ошибке
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:  # with open то контекстный менеджер,
                        # который автоматически открывает файл и закрывает его после
                        # завершения работы с ним
                        f.write(f"{message}\n")
                        # f.write(f"{massage},\n") используется для записи строки message в файл

                else:
                    print(message)

                raise  # Что вроде блока "успех" записывает в файл или выводит в консоль

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


@log()
def error_function(x):
    if x < 0:
        raise ValueError("Отрицательное число")
    return x**2
