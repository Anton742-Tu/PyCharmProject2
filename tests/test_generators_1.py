import pytest
from typing import Dict, Any, List
from src.generators import transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями (корректные и некорректные)."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Покупка валюты"},
        {"id": 3},  # Нет описания
        {"id": 4, "description": None},  # Описание = None
        {"id": 5, "description": 12345},  # Не строка
        {"id": 6, "description": "Снятие наличных"},
    ]


def test_transaction_descriptions() -> None:
    # Подготовка тестовых данных
    transactions = [
        {"description": "Payment 1"},
        {"description": "Payment 2"},
        {},  # Нет описания
        {"description": None},  # None вместо описания
        {"description": "Payment 3"},
    ]

    # Тест 1: Получение всех описаний
    result = list(transaction_descriptions(transactions))
    assert result == ["Payment 1", "Payment 2", "Payment 3"], "Должны вернуться только строковые описания"

    # Тест 2: Пустой список транзакций
    result = list(transaction_descriptions([]))
    assert len(result) == 0, "Для пустого списка должен вернуться пустой результат"

    # Тест 3: Транзакции без описаний
    transactions = [{}, {"amount": 100}]
    result = list(transaction_descriptions(transactions))
    assert len(result) == 0, "Нет описаний - должен вернуться пустой список"


def test_transaction_descriptions_valid(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест корректных описаний (только строки)."""
    generator = transaction_descriptions(sample_transactions)
    expected_descriptions = ["Перевод организации", "Покупка валюты", "Снятие наличных"]
    assert list(generator) == expected_descriptions


def test_transaction_descriptions_empty_list() -> None:
    """Тест пустого списка транзакций."""
    generator = transaction_descriptions([])
    assert list(generator) == []


def test_transaction_descriptions_no_description(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест транзакций без описания (пропускаются)."""
    # Выбираем только транзакции без description или с некорректным типом
    invalid_transactions = [tx for tx in sample_transactions if not isinstance(tx.get("description"), str)]
    generator = transaction_descriptions(invalid_transactions)
    assert list(generator) == []


@pytest.mark.parametrize(
    "description, expected",
    [
        ("Оплата налогов", ["Оплата налогов"]),  # Корректная строка
        (None, []),  # None пропускается
        (123, []),  # Не строка
        ("", [""]),  # Пустая строка (допустимо)
    ],
)
def test_transaction_descriptions_parametrized(description: Any, expected: List[str]) -> None:
    """Параметризованный тест для разных типов description."""
    transactions = [{"id": 1, "description": description}]
    generator = transaction_descriptions(transactions)
    assert list(generator) == expected


@pytest.mark.parametrize(
    "transactions,expected",
    [
        ([{"description": "Test"}], ["Test"]),
        ([{"description": "A"}, {"description": "B"}], ["A", "B"]),
        ([{}], []),
    ],
)
def test_transaction_descriptions_cases(transactions, expected):
    assert list(transaction_descriptions(transactions)) == expected


def test_non_string_descriptions() -> None:
    transactions = [
        {"description": "Valid"},
        {"description": 123},  # Number
        {"description": {"key": "value"}},  # Dict
    ]
    result = list(transaction_descriptions(transactions))
    assert result == ["Valid"], "Должен игнорировать нестроковые описания"


def test_long_description() -> None:
    long_text = "A" * 1000  # Very long description
    transactions = [{"description": long_text}]
    result = list(transaction_descriptions(transactions))
    assert result == [long_text], "Должен поддерживать длинные описания"
