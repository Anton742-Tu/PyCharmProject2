from datetime import datetime
from typing import Dict, Union, List

# Константы
ACCOUNT_VISIBLE_DIGITS: int = 4
CARD_NUMBER_LENGTHS: Dict[str, Union[int, List[int]]] = {
    "visa": [13, 16],
    "mastercard": 16,
    "maestro": [12, 13, 14, 15, 16, 17, 18, 19],
    "american express": 15,
    "mir": 16,
}

# Словарь поддерживаемых типов (регистр-независимо)
SUPPORTED_TYPES: Dict[str, str] = {
    # Карты (русский + английский)
    "карта": "card",
    "card": "card",
    "visa": "visa",
    "виза": "visa",
    "mastercard": "mastercard",
    "мастеркард": "mastercard",
    "маэстро": "maestro",
    "maestro": "maestro",
    "american express": "american express",
    "американ экспресс": "american express",
    "мир": "mir",
    "mir": "mir",
    # Счета
    "счёт": "account",
    "счет": "account",  # альтернативное написание
    "account": "account",
}


def mask_account_card(data: str) -> str:
    """
    Маскирует номер карты или счёта в переданной строке.
    - American Express (15 Цифр): XXXX XXXXXX XXXXX
    - Другие карты (16 цифр): XXXX XX** **** XXXX
    - Счета: **XXXX
    Возвращает маскированную строку или сообщение об ошибке.
    """
    if not data:
        return "Ошибка: Пустой ввод."

    # Разделяем тип и номер (регистр-независимо)
    parts = data.strip().split()
    if len(parts) < 2:
        return "Ошибка: Неверный формат. Ожидается '[Тип] [Номер]'."

    data_type = " ".join(parts[:-1]).lower()  # Объединяем все части, кроме номера (для "American Express")
    number = parts[-1].replace(" ", "")

    # Определяем тип (поддержка разных языков и сложных названий)
    normalized_type = SUPPORTED_TYPES.get(data_type)
    if not normalized_type:
        return "Ошибка: Неподдерживаемый тип. Используйте: 'Visa', 'Visa Platinum', 'Visa Gold', 'Visa Classic'\
         'Mastercard', 'Maestro', 'American Express', 'Мир', 'Счёт'."

    # Проверяем, что номер состоит только из цифр
    if not number.isdigit():
        return "Ошибка: Номер должен содержать только цифры."

    # Маскировка для карт
    if normalized_type in CARD_NUMBER_LENGTHS:
        required_lengths = CARD_NUMBER_LENGTHS[normalized_type]
        if isinstance(required_lengths, int):
            required_lengths = [required_lengths]

        if len(number) not in required_lengths:
            return f"Ошибка: Номер {normalized_type} должен содержать {required_lengths} цифр."

        # Специальный формат для American Express (15 цифр)
        if normalized_type == "american express":
            masked_number = f"{number[:4]} {number[4:6]}**** **{number[-3:]}"
        else:
            # Стандартный формат для 16-значных карт
            masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"

        return f"{data_type.title()} {masked_number}"

    # Маскировка для счетов
    elif normalized_type == "account":
        if len(number) < ACCOUNT_VISIBLE_DIGITS:
            return f"Ошибка: Номер счёта должен содержать минимум {ACCOUNT_VISIBLE_DIGITS} цифр."
        return f"Счёт **{number[-ACCOUNT_VISIBLE_DIGITS:]}"

    else:
        return "Ошибка: Неизвестный тип данных."


def get_date(iso_date: str) -> str:
    """
    Преобразует дату из формата ISO ("2024-03-11T02:26:18.671407") в "ДД.ММ.ГГГГ" ("11.03.2024").
    Если формат некорректный, возвращает сообщение об ошибке.
    """
    try:
        # Обрабатываем дату из строки
        date_obj = datetime.strptime(iso_date.split(".")[0], "%Y-%m-%dT%H:%M:%S")
        return date_obj.strftime("%d.%m.%Y")
    except (ValueError, AttributeError):
        return "Ошибка: Некорректный формат даты. Ожидается 'ГГГГ-ММ-ДДTЧЧ:ММ:СС'."
