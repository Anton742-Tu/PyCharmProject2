from src.widget import mask_account_card, get_date


def test_mask_account_card() -> None:
    """Тестирует маскировку карт и счетов."""
    # Тест для карт
    assert mask_account_card("Visa 1234567890123456") == "Visa 1234 56** **** 3456"
    assert mask_account_card("Mastercard 1234567890123456") == "Mastercard 1234 56** **** 3456"
    assert mask_account_card("Maestro 1234567890123456") == "Maestro 1234 56** **** 3456"
    assert mask_account_card("American Express 123456789012345") == "American Express 1234 56**** **345"
    assert mask_account_card("Мир 1234567890123456") == "Мир 1234 56** **** 3456"

    # Тест для счетов
    assert mask_account_card("Счёт 1234567890") == "Счёт **7890"
    assert mask_account_card("Account 1234567890") == "Счёт **7890"

    # Тест ошибок
    assert "Ошибка" in mask_account_card("Visa 123")  # Слишком короткий номер
    assert "Ошибка" in mask_account_card("Card 1234567890ABCD")  # Не цифры
    assert "Ошибка" in mask_account_card("InvalidType 1234567890")  # Неподдерживаемый тип


def test_get_date() -> None:
    """
    Тестирует форматирование даты.
    """
    # Корректные форматы
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("1999-12-31T23:59:59.999999") == "31.12.1999"

    # Ошибки
    assert (
        get_date("2024-03-11") == "Ошибка: Некорректный формат даты. Ожидается 'ГГГГ-ММ-ДДTЧЧ:ММ:СС'."
    )  # Нет времени
    assert (
        get_date("не дата") == "Ошибка: Некорректный формат даты. Ожидается 'ГГГГ-ММ-ДДTЧЧ:ММ:СС'."
    )  # Неправильный ввод
