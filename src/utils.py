import json
import logging
from typing import List, Dict, Any
from pathlib import Path


# Настройка логера
def setup_utils_logger() -> logging.Logger:
    # Создаем папку logs если ее нет
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Создаем логер
    logger = logging.getLogger("utils")
    logger.setLevel(logging.DEBUG)  # Уровень не ниже DEBUG

    # Форматтер для логов
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # FileHandler для записи в файл (перезаписываем при каждом запуске)
    file_handler = logging.FileHandler(filename=logs_dir / "utils.log", mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Добавляем handler к логеру
    logger.addHandler(file_handler)

    return logger


# Инициализация логгера
utils_logger: logging.Logger = setup_utils_logger()


def read_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список транзакций.
    В случае ошибок возвращает пустой список.
    """
    try:
        utils_logger.debug(f"Начало чтения файла: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            data: Any = json.load(file)

            if not isinstance(data, list):
                utils_logger.warning(
                    f"Файл {file_path} не содержит список транзакций. " f"Получен тип: {type(data).__name__}"
                )
                return []

            utils_logger.info(f"Успешно прочитано {len(data)} транзакций из {file_path}")
            return data

    except FileNotFoundError as e:
        utils_logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        utils_logger.error(f"Ошибка декодирования JSON в файле {file_path}: {str(e)}")
        return []
    except Exception as e:
        utils_logger.critical(f"Неожиданная ошибка при чтении {file_path}", exc_info=True)
        return []


def write_transactions_to_json(transactions: List[Dict[str, Any]], file_path: str) -> bool:
    """
    Записывает список транзакций в JSON-файл.
    Возвращает True при успешной записи, False при ошибке.
    """
    try:
        utils_logger.debug(f"Начало записи в файл: {file_path}")

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=2, ensure_ascii=False)

        utils_logger.info(f"Успешно записано {len(transactions)} транзакций в {file_path}")
        return True

    except Exception as e:
        utils_logger.error(f"Ошибка записи в файл {file_path}: {str(e)}", exc_info=True)
        return False
