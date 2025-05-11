import pytest
from typing import Dict, Any, List
from src.generators import filter_by_currency


def test_filter_bay_currency() -> None:
    # Подготовка тестовых данных
    transactions = [
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "EUR"}}},
        {"operationAmount": {"currency": {"code": "USD"}}},
    ]

    # Тест 1: Фильтрация по USD
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2, "Должно быть 2 USD транзакции"

    # Тест 2: Фильтрация по EUR
    result = list(filter_by_currency(transactions, "EUR"))
    assert len(result) == 1, "Должна быть 1 EUR транзакция"

    # Тест 3: Фильтрация по несуществующей валюте
    result = list(filter_by_currency(transactions, "RUB"))
    assert len(result) == 0, "Не должно быть RUB транзакций"

    # Тест 4: Пустой список транзакций
    result = list(filter_by_currency([], "USD"))
    assert len(result) == 0, "Для пустого списка должен вернуться пустой результат"


@pytest.fixture
def transactions_fixture() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        # Корректные транзакции
        {"id": 1, "operationAmount": {"amount": "100.00", "currency": {"code": "USD", "name": "Доллар"}}},
        {"id": 2, "operationAmount": {"amount": "200.00", "currency": {"code": "EUR", "name": "Евро"}}},
        {"id": 3, "operationAmount": {"amount": "300.00", "currency": {"code": "USD", "name": "Доллар"}}},
        # Некорректные/неполные транзакции
        {"id": 4, "operationAmount": {"amount": "400.00"}},  # Нет currency
        {"id": 5},  # Нет operationAmount
    ]


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [1, 3]),  # Ожидаются транзакции с ID 1 и 3
        ("EUR", [2]),  # Ожидается транзакция с ID 2
        ("RUB", []),  # Нет подходящих транзакций
        ("GBP", []),  # Нет подходящих транзакций
    ],
)
def test_filter_by_currency(
    transactions_fixture: List[Dict[str, Any]],
    currency: str,
    expected_ids: List[int],
) -> None:
    """Тест фильтрации транзакций по валюте."""
    result = list(filter_by_currency(transactions_fixture, currency))
    assert len(result) == len(expected_ids)
    assert all(tx["id"] in expected_ids for tx in result)


def test_filter_by_currency_empty_input() -> None:
    """Тест на пустом списке транзакций."""
    assert list(filter_by_currency([], "USD")) == []


def test_filter_by_currency_invalid_structure() -> None:
    """Тест с транзакциями, у которых нет поля currency."""
    transactions = [
        {"id": 1, "operationAmount": {"amount": "100.00"}},
        {"id": 2, "operationAmount": {"amount": "200.00", "currency": {"code": "USD"}}},
    ]
    assert list(filter_by_currency(transactions, "USD")) == [transactions[1]]


def test_filter_multiple_currencies() -> None:
    """Тестирование фильтрации при смешанных валютах."""
    transactions = [
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "EUR"}}},
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"amount": "100.00"}},  # Нет currency
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2
    assert all(tx["operationAmount"]["currency"]["code"] == "USD" for tx in result)


@pytest.mark.parametrize("transaction,currency,expected", [
    # Полная корректная структура
    (
        {
            "operationAmount": {
                "currency": {"code": "USD", "name": "Доллар"}
            }
        },
        "USD",
        True
    ),
    # Нет поля currency
    (
        {"operationAmount": {"amount": "100.00"}},
        "USD",
        False
    ),
    # Нет operationAmount
    (
        {"id": 1},
        "USD",
        False
    ),
    # Currency как строка вместо словаря
    (
        {"operationAmount": {"currency": "USD"}},
        "USD",
        False
    ),
    # Пустой словарь currency
    (
        {"operationAmount": {"currency": {}}},
        "USD",
        False
    ),
    # Несколько уровней вложенности
    (
        {"data": {"operationAmount": {"currency": {"code": "EUR"}}}},
        "EUR",
        False  # Не будет найдено из-за неправильного пути
    ),
])
def test_filter_edge_cases(transaction: Dict[str, Any], currency: str, expected: bool):
    """Тестирование различных структур транзакций."""
    result = list(filter_by_currency([transaction], currency))
    assert (len(result) == 1) == expected


def test_filter_invalid_input_types() -> None:
    """Тестирование обработки некорректных типов входных данных."""
    # 1. Проверка неверного типа transactions
    with pytest.raises(TypeError, match="transactions должен быть списком"):
        list(filter_by_currency("not a list", "USD"))

    # 2. Проверка неверного типа currency
    with pytest.raises(TypeError, match="currency должен быть строкой из 3 символов"):
        list(filter_by_currency([], 123))

    # 3. Проверка неверной длины currency
    with pytest.raises(TypeError, match="currency должен быть строкой из 3 символов"):
        list(filter_by_currency([], "US"))  # 2 символа
    with pytest.raises(TypeError):
        list(filter_by_currency([], "USDX"))  # 4 символа
