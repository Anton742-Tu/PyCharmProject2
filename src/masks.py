import logging
from pathlib import Path
from typing import Union
import os

# Константы
CARD_NUMBER_LENGTH: int = 16
VISIBLE_DIGITS: int = 4
LOG_DIR: str = "logs"
LOG_FILE: str = "masks.log"

# Создаем логгер
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)  # Устанавливаем уровень не ниже DEBUG

# Создаем папку для логов, если ее нет
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

# Создаем file handler с указанием кодировки UTF-8
file_handler = logging.FileHandler(
    filename=os.path.join(LOG_DIR, LOG_FILE),
    mode="w",  # Перезаписываем файл при каждом запуске
    encoding="utf-8",  # Явно указываем кодировку UTF-8
)
file_handler.setLevel(logging.DEBUG)

# Форматтер с указанием времени, имени модуля, уровня и сообщения
file_formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)

# Добавляем handler к логгеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Маскирует номер карты в формате 'XXXX XX** **** XXXX'."""
    try:
        str_number: str = str(card_number).replace(" ", "")

        logger.debug(f"Начало маскирования номера карты. Входные данные: {str_number}")

        if len(str_number) != CARD_NUMBER_LENGTH or not str_number.isdigit():
            error_msg = "Некорректный номер карты"
            logger.error(f"{error_msg}. Получено: {str_number}")
            return error_msg

        masked_number = f"{str_number[:4]} {str_number[4:6]}** **** {str_number[-4:]}"
        logger.info(f"Успешное маскирование номера карты. Результат: {masked_number}")
        return masked_number

    except Exception as e:
        logger.exception(f"Ошибка при маскировании номера карты: {str(card_number)} {str(e)}")
        return "Ошибка при обработке номера карты"


def get_mask_account(account_number: Union[str, int]) -> str:
    """Маскирует номер счёта в формате '**XXXX'."""
    try:
        str_number: str = str(account_number).replace(" ", "")

        logger.debug(f"Начало маскирования номера счета. Входные данные: {str_number}")

        if not str_number.isdigit() or not str_number:
            error_msg = "Некорректный номер счёта"
            logger.error(f"{error_msg}. Получено: {str_number}")
            return error_msg

        if len(str_number) < VISIBLE_DIGITS:
            error_msg = f"Номер слишком короткий (минимум {VISIBLE_DIGITS} цифры)"
            logger.error(f"{error_msg}. Получено: {str_number}")
            return error_msg

        masked_number = f"**{str_number[-VISIBLE_DIGITS:]}"
        logger.info(f"Успешное маскирование номера счета. Результат: {masked_number}")
        return masked_number

    except Exception as e:
        logger.exception(f"Ошибка при маскировании номера счета: {str(account_number)} {str(e)}")
        return "Ошибка при обработке номера счета"
