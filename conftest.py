from typing import Tuple
import pytest
from src.masks import get_mask_card_number, get_mask_account


# Фикстуры для тестовых данных
@pytest.fixture(
    params=[
        ("1234567890123456", "1234 56** **** 3456"),
        ("1234 5678 9012 3456", "1234 56** **** 3456"),
        ("1234", "Некорректный номер карты"),
        ("abcdefghijklmnop", "Некорректный номер карты"),
        ("12345678901234567890", "Некорректный номер карты"),
])
def card_test_cases(request: pytest.FixtureRequest) -> Tuple[str, str]:
    return request.param


@pytest.fixture(
    params=[
        ("123456", "**3456"),
        ("1234 5678", "**5678"),
        ("12", "Номер слишком короткий (минимум 4 цифры)"),
        ("abcdef", "Некорректный номер счёта"),
        ("1234567890", "**7890"),
])
def account_test_cases(request: pytest.FixtureRequest) -> Tuple[str, str]:
    return request.param


# Параметризированные тесты для карт
def test_card_masking(card_test_cases: Tuple[int, str]) -> None:
    input_data, expected = card_test_cases
    result = get_mask_card_number(input_data)
    assert result == expected, f"Для входа {input_data} ожидалось {expected}, получено {result}"


# Параметризированные тесты для счетов
def test_account_masking(account_test_cases: Tuple[int, str]) -> None:
    input_data, expected = account_test_cases
    result = get_mask_account(input_data)
    assert result == expected, f"Для входа {input_data} ожидалось {expected}, получено {result}"
