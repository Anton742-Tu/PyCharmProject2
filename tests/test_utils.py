import pytest
from unittest.mock import patch, Mock
import json

import requests

from src.utils import read_transactions_from_json
from src.external_api import get_amount_in_rub


# Основные тесты для корректных случаев
def test_rub_transaction():
    """Транзакция в RUB должна возвращать ту же сумму."""
    transaction = {"amount": "100.50", "currency": "RUB"}
    assert get_amount_in_rub(transaction) == 100.50


def test_usd_transaction_with_mock():
    """Транзакция в USD должна конвертироваться по курсу."""
    # Мокаем ответ API
    mock_response = Mock()
    mock_response.json.return_value = {
        "rates": {"USD": 0.011, "EUR": 0.0095},
        "base": "RUB",
        "date": "2023-01-01"
    }

    with patch('requests.get', return_value=mock_response):
        transaction = {"amount": 100, "currency": "USD"}
        # 100 USD * (1 / 0.011) ≈ 9090.91 RUB
        assert get_amount_in_rub(transaction) == pytest.approx(9090.91, rel=1e-2)


def test_eur_transaction_with_mock():
    """Транзакция в EUR должна конвертироваться по курсу."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "rates": {"USD": 0.011, "EUR": 0.0095},
        "base": "RUB",
        "date": "2023-01-01"
    }

    with patch('requests.get', return_value=mock_response):
        transaction = {"amount": "200", "currency": "EUR"}
        # 200 EUR * (1 / 0.0095) ≈ 21052.63 RUB
        assert get_amount_in_rub(transaction) == pytest.approx(21052.63, rel=1e-2)


# Тесты для обработки ошибок
def test_invalid_currency():
    """Неизвестная валюта должна вызывать ValueError."""
    transaction = {"amount": 100, "currency": "GBP"}
    with pytest.raises(ValueError, match="Неподдерживаемая валюта: GBP"):
        get_amount_in_rub(transaction)


def test_api_error_handling():
    """Ошибка API должна вызывать RequestException."""
    with patch('requests.get', side_effect=requests.RequestException("API недоступен")):
        transaction = {"amount": 100, "currency": "USD"}
        with pytest.raises(requests.RequestException, match="Ошибка при получении курсов валют"):
            get_amount_in_rub(transaction)


def test_invalid_api_response():
    """Неверный формат ответа API должен вызывать KeyError."""
    mock_response = Mock()
    mock_response.json.return_value = {"wrong": "format"}  # Нет поля 'rates'

    with patch('requests.get', return_value=mock_response):
        transaction = {"amount": 100, "currency": "EUR"}
        with pytest.raises(KeyError, match="Неверный формат ответа от API"):
            get_amount_in_rub(transaction)


# Дополнительные тесты для граничных случаев
def test_zero_amount():
    """Сумма 0 должна возвращать 0 в любой валюте."""
    transaction = {"amount": "0", "currency": "USD"}
    with patch('requests.get'):  # Мок API не важен, так как сумма 0
        assert get_amount_in_rub(transaction) == 0.0


def test_negative_amount():
    """Отрицательная сумма должна корректно конвертироваться."""
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"USD": 0.011}, "base": "RUB"}

    with patch('requests.get', return_value=mock_response):
        transaction = {"amount": -50, "currency": "USD"}
        assert get_amount_in_rub(transaction) == pytest.approx(-4545.45, rel = 1e-2)


# Тесты
def test_read_normal_transactions(tmp_path):
    """Тест корректного файла с транзакциями"""
    test_data = [
        {"id": 1, "amount": 100.50, "description": "Покупка продуктов"},
        {"id": 2, "amount": 200.75, "description": "Оплата услуг"}
    ]

    file_path = tmp_path / "transactions.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)

    result = read_transactions_from_json(file_path)
    assert result == test_data
    assert len(result) == 2


def test_file_not_found():
    """Тест случая, когда файл не существует"""
    result = read_transactions_from_json("nonexistent_file.json")
    assert result == []


def test_empty_file(tmp_path):
    """Тест пустого файла"""
    file_path = tmp_path / "empty.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("")

    result = read_transactions_from_json(file_path)
    assert result == []


def test_invalid_json(tmp_path):
    """Тест файла с невалидным JSON"""
    file_path = tmp_path / "invalid.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("{invalid json}")

    result = read_transactions_from_json(file_path)
    assert result == []


def test_not_a_list(tmp_path):
    """Тест случая, когда JSON содержит не список"""
    file_path = tmp_path / "not_a_list.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump({"key": "value"}, f)

    result = read_transactions_from_json(file_path)
    assert result == []


def test_large_transactions_file(tmp_path):
    """Тест с большим файлом транзакций"""
    test_data = [{"id": i, "amount": i * 10} for i in range(1000)]

    file_path = tmp_path / "large.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)

    result = read_transactions_from_json(file_path)
    assert len(result) == 1000
    assert result[999]["amount"] == 9990