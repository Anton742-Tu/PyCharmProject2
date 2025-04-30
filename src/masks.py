# Константы
CARD_NUMBER_LENGTH = 16
VISIBLE_DIGITS = 4


def get_mask_card_number(card_number: int) -> str:

    # Преобразуем номер карты в строку
    str_number = str(card_number).replace(" ", "")

    # Проверяем, что номер карты состоит из 16 цифр
    if len(str_number) != CARD_NUMBER_LENGTH or not str_number.isdigit():
        return "Некорректный номер карты"

    # Форматируем номер карты по маске xxxx xx** **** xxxx
    masked_number = f"{str_number[:4]} {str_number[4:6]}** **** {str_number[-4:]}"

    return masked_number


def get_mask_account(account_number: int) -> str:

    # Преобразуем номер счёта в строку и удаляем пробелы
    str_number = str(account_number).replace(" ", "")

    # Проверяем, что номер состоит только из цифр и не пустой
    if not str_number.isdigit() or not str_number:
        return "Некорректный номер счёта"

    # Проверяем, что номер достаточно длинный
    if len(str_number) < VISIBLE_DIGITS:
        return f"Номер слишком короткий (минимум {VISIBLE_DIGITS} цифры)"

    # Маскируем: ** + последние VISIBLE_DIGITS цифр
    masked_number = f"**{str_number[-VISIBLE_DIGITS:]}"

    return masked_number
