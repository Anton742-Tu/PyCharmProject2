import pytest
from typing import Dict, Any, List
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


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
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с различными типами транзакций для тестирования"""
    return [
        # Стандартные случаи
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}},
        {"id": 3, "operationAmount": {"currency": {"code": "USD", "name": "Доллар"}}},

        # Крайние случаи
        {"id": 4},  # Нет operationAmount
        {"id": 5, "operationAmount": None},  # operationAmount = None
        {"id": 6, "operationAmount": {"amount": "100"}},  # Нет currency
        {"id": 7, "operationAmount": {"currency": None}},  # currency = None
        {"id": 8, "operationAmount": {"currency": {"name": "Доллар"}}},  # Нет code
        {"id": 9, "operationAmount": {"currency": "USD"}},  # currency как строка
        {"id": 10, "operationAmount": {"currency": {"code": 840}}},  # code как число
    ]


@pytest.mark.parametrize("currency, expected_ids", [
    ("USD", [1, 3]),  # Стандартные USD транзакции
    ("EUR", [2]),  # Стандартные EUR транзакции
    ("RUB", []),  # Нет RUB транзакций
    ("GBP", []),  # Нет GBP транзакций
])
def test_standard_cases(
        sample_transactions: List[Dict[str, Any]],
        currency: str,
        expected_ids: List[int]
) -> None:
    """Тестирование стандартных случаев фильтрации"""
    result = list(filter_by_currency(sample_transactions, currency))
    assert [tx["id"] for tx in result] == expected_ids


def test_edge_cases(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тестирование крайних случаев"""
    # Все некорректные транзакции должны быть проигнорированы
    assert len(list(filter_by_currency(sample_transactions, "USD"))) == 2
    assert len(list(filter_by_currency(sample_transactions, "EUR"))) == 1


def test_empty_input() -> None:
    """Тестирование пустого ввода"""
    assert list(filter_by_currency([], "USD")) == []


def test_currency_case_sensitivity() -> None:
    """Тестирование чувствительности к регистру"""
    transactions = [{"operationAmount": {"currency": {"code": "usd"}}}]
    # В зависимости от требований - должен ли код валюты быть в верхнем регистре
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0  # или 1, если функция нечувствительна к регистру


def test_nested_transaction_structures() -> None:
    """Тестирование вложенных структур"""
    transactions = [
        {"data": {"operation": {"amount": {"currency": {"code": "USD"}}}}}
    ]
    # В зависимости от реализации функции
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0  # или 1, если функция поддерживает глубокий поиск


def test_performance_large_dataset() -> None:
    """Тестирование производительности на большом наборе данных"""
    large_transactions = [{"operationAmount": {"currency": {"code": "USD"}}}] * 10000
    result = list(filter_by_currency(large_transactions, "USD"))
    assert len(result) == 10000


@pytest.fixture
def transactions_fixture() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями (корректные и некорректные)."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Покупка валюты"},
        {"id": 3},  # Нет описания
        {"id": 4, "description": None},  # Описание = None
        {"id": 5, "description": 12345},  # Не строка
        {"id": 6, "description": "Снятие наличных"},
    ]


def test_transaction_descriptions_valid(transactions_fixture: List[Dict[str, Any]]) -> None:
    """Тест корректных описаний (только строки)."""
    generator = transaction_descriptions(transactions_fixture)
    expected_descriptions = ["Перевод организации", "Покупка валюты", "Снятие наличных"]
    assert list(generator) == expected_descriptions


def test_transaction_descriptions_empty_list() -> None:
    """Тест пустого списка транзакций."""
    generator = transaction_descriptions([])
    assert list(generator) == []


def test_transaction_descriptions_no_description(transactions_fixture: List[Dict[str, Any]]) -> None:
    """Тест транзакций без описания (пропускаются)."""
    # Выбираем только транзакции без description или с некорректным типом
    invalid_transactions = [tx for tx in transactions_fixture if not isinstance(tx.get("description"), str)]
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
    "transactions, expected",
    [
        ([{"description": "Test"}], ["Test"]),
        ([{"description": "A"}, {"description": "B"}], ["A", "B"]),
        ([{}], []),
    ],
)
def test_transaction_descriptions_cases(transactions: Any, expected: List[str]) -> None:
    assert list(transaction_descriptions(transactions)) == expected


def test_long_description() -> None:
    long_text = "A" * 1000  # Very long description
    transactions = [{"description": long_text}]
    result = list(transaction_descriptions(transactions))
    assert result == [long_text], "Должен поддерживать длинные описания"


def test_card_number_generator() -> None:
    # Тест 1: Генерация одного номера
    gen = card_number_generator(1, 1)
    assert next(gen) == "0000 0000 0000 0001", "Первый номер должен быть 0000 0000 0000 0001"

    # Тест 2: Генерация диапазона
    gen = card_number_generator(1, 3)
    assert list(gen) == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
    ], "Должны сгенерироваться три последовательных номера"

    # Тест 3: Проверка формата
    gen = card_number_generator(1234567812345678, 1234567812345678)
    number = next(gen)
    assert len(number) == 19, "Длина номера должна быть 19 символов (16 цифр + 3 пробела)"
    assert number.count(" ") == 3, "Должно быть 3 пробела"
    assert number.replace(" ", "").isdigit(), "Должны быть только цифры"

    # Тест 4: Некорректный диапазон (start > end)
    try:
        list(card_number_generator(10, 1))
        assert False, "Должно было возникнуть ValueError"
    except ValueError:
        pass  # Ожидаемое поведение

    # Тест 5: Граничные значения
    gen = card_number_generator(9999999999999999, 9999999999999999)
    assert next(gen) == "9999 9999 9999 9999", "Последний номер должен быть 9999 9999 9999 9999"


@pytest.mark.parametrize(
    "start, end, expected_numbers",
    [
        (
            1,
            3,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
            ],
        ),
        (
            9999,
            10001,
            [
                "0000 0000 0000 9999",
                "0000 0000 0001 0000",
                "0000 0000 0001 0001",
            ],
        ),
    ],
)
def test_card_number_generator_range(
    start: int,
    end: int,
    expected_numbers: list[str],
) -> None:
    """Тест генерации номеров карт в заданном диапазоне."""
    generator = card_number_generator(start, end)
    generated_numbers = list(generator)
    assert generated_numbers == expected_numbers


def test_card_number_generator_format() -> None:
    """Тест формата номера карты (16 цифр, разделённых пробелами)."""
    generator = card_number_generator(1234567890123456, 1234567890123456)
    number = next(generator)
    assert len(number) == 19  # 16 цифр + 3 пробела
    assert number.replace(" ", "").isdigit()


def test_card_number_generator_invalid_range() -> None:
    """Тест на некорректный диапазон (start > end)."""
    with pytest.raises(ValueError, match="Start must be less than or equal to end"):
        list(card_number_generator(10, 1))


def test_card_number_generator_edge_cases() -> None:
    """Тест граничных случаев (минимальный и максимальный номера)."""
    # Первый номер
    assert next(card_number_generator(1, 1)) == "0000 0000 0000 0001"
    # Последний номер
    assert next(card_number_generator(9999999999999999, 9999999999999999)) == "9999 9999 9999 9999"


def test_large_range() -> None:
    gen = card_number_generator(1, 100)
    result = list(gen)
    assert len(result) == 100, "Должен генерировать большой диапазон"
    assert result[0] == "0000 0000 0000 0001", "Первый номер должен быть корректным"
    assert result[-1] == "0000 0000 0000 0100", "Последний номер должен быть корректным"


def test_spacing_in_numbers() -> None:
    gen = card_number_generator(1234567812345678, 1234567812345678)
    number = next(gen)
    parts = number.split(" ")
    assert len(parts) == 4, "Должно быть 4 группы цифр"
    assert all(len(part) == 4 for part in parts), "Каждая группа должна содержать 4 цифры"
