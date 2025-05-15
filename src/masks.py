from typing import Union


# Константы
CARD_NUMBER_LENGTH: int = 16
VISIBLE_DIGITS: int = 4


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Маскирует номер карты в формате 'XXXX XX** **** XXXX'."""
    str_number: str = str(card_number).replace(" ", "")

    # Проверяем, что номер карты состоит из 16 цифр
    if len(str_number) != CARD_NUMBER_LENGTH or not str_number.isdigit():
        return "Некорректный номер карты"

    # Форматируем номер карты по маске xxxx xx** **** xxxx
    masked_number = f"{str_number[:4]} {str_number[4:6]}** **** {str_number[-4:]}"

    return masked_number


def get_mask_account(account_number: Union[str, int]) -> str:
    """Маскирует номер счёта в формате '**XXXX'."""
    str_number: str = str(account_number).replace(" ", "")

    # Проверяем, что номер состоит только из цифр и не пустой
    if not str_number.isdigit() or not str_number:
        return "Некорректный номер счёта"

    # Проверяем, что номер достаточно длинный
    if len(str_number) < VISIBLE_DIGITS:
        return f"Номер слишком короткий (минимум {VISIBLE_DIGITS} цифры)"

    # Маскируем: ** + последние VISIBLE_DIGITS цифр
    masked_number = f"**{str_number[-VISIBLE_DIGITS:]}"

    return masked_number
