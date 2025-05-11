from typing import Any, Tuple

import pytest

from src.masks import get_mask_card_number, get_mask_account
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


# Фикстуры для тестовых данных
@pytest.fixture
def card_test_cases(request: pytest.FixtureRequest) -> Any:
    cases = [
        ("1234567890123456", "1234 56** **** 3456"),
        ("1234 5678 9012 3456", "1234 56** **** 3456"),
        ("1234", "Некорректный номер карты"),
        ("abcdefghijklmnop", "Некорректный номер карты"),
        ("12345678901234567890", "Некорректный номер карты"),
    ]
    return cases[request.param_index] if hasattr(request, "param_index") else cases[0]


@pytest.fixture
def account_test_cases(request: pytest.FixtureRequest) -> Any:
    cases = [
        ("123456", "**3456"),
        ("1234 5678", "**5678"),
        ("12", "Номер слишком короткий (минимум 4 цифры)"),
        ("abcdef", "Некорректный номер счёта"),
        ("1234567890", "**7890"),
    ]
    return cases[request.param_index] if hasattr(request, "param_index") else cases[0]


# Параметризированные тесты для карт
def test_card_masking(card_test_cases: Tuple[str, str]) -> None:
    input_data, expected = card_test_cases
    result: str = get_mask_card_number(input_data)
    assert result == expected, f"Для входа {input_data} ожидалось {expected}, получено {result}"


# Параметризированные тесты для счетов
def test_account_masking(account_test_cases: Tuple[str, str]) -> None:
    input_data, expected = account_test_cases
    result: str = get_mask_account(input_data)
    assert result == expected, f"Для входа {input_data} ожидалось {expected}, получено {result}"


# Дополнительные тесты с прямой параметризацией
@pytest.mark.parametrize(
    "input_data,expected",
    [
        ("", "Некорректный номер счёта"),
        ("1" * 3, "Номер слишком короткий (минимум 4 цифры)"),
        ("1" * 4, "**1111"),
        ("1" * 10, "**1111"),  # Проверка, что берутся последние 4 цифры
    ],
)
def test_edge_cases_account(input_data: str, expected: str) -> None:
    result: str = get_mask_account(input_data)
    assert result == expected
