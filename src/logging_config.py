import logging
import os


def setup_logger(module_name: str) -> logging.Logger:
    """
    Создаёт и настраивает логгер для указанного модуля.
    """
    # Создаём путь к папке логов
    log_folder = os.path.join("logs")
    os.makedirs(log_folder, exist_ok=True)
    log_file_path = os.path.join(log_folder, f"{module_name}.log")

    # Создаём логгер
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    # Очищаем существующие обработчики
    logger.handlers.clear()

    # Обработчик для записи в файл (режим 'w' — перезапись при каждом запуске)
    file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # Форматировщик
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger


# Создаём логгеры для модулей
masks_logger = setup_logger("masks")
utils_logger = setup_logger("utils")
