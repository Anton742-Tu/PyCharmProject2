import pytest
from unittest.mock import patch
from pathlib import Path
import pandas as pd
from src.finance_reader import read_financial_transactions


def test_read_csv_file() -> None:
    """Тест чтения CSV-файла с моком pandas.read_csv."""
    # Подготовка тестовых данных
    test_data = [
        {"id": 1, "amount": 100, "description": "Покупка"},
        {"id": 2, "amount": 200, "description": "Продажа"},
    ]
    test_df = pd.DataFrame(test_data)

    # Мокируем:
    # 1) Path.exists (чтобы файл "существовал")
    # 2) pd.read_csv (возвращает тестовый DataFrame)
    with patch("pathlib.Path.exists", return_value=True), patch(
        "pandas.read_csv", return_value=test_df
    ) as mock_read_csv:
        # Вызываем тестируемую функцию
        result = read_financial_transactions("test.csv")

        # Проверяем, что pd.read_csv вызван с правильным путем
        mock_read_csv.assert_called_once()
        assert isinstance(mock_read_csv.call_args[0][0], Path)  # Проверяем, что передан Path

        # Проверяем, что возвращаемые данные верны
        assert result == test_data


def test_read_excel_file() -> None:
    """Тест чтения Excel-файла с моком pandas.read_excel."""
    test_data = [
        {"id": 1, "amount": 150, "description": "Доход"},
        {"id": 2, "amount": -50, "description": "Расход"},
    ]
    test_df = pd.DataFrame(test_data)

    # Мокируем:
    # 1) Path.exists (чтобы файл "существовал")
    # 2) pd.read_excel (возвращает тестовый DataFrame)
    with patch("pathlib.Path.exists", return_value=True), patch(
        "pandas.read_excel", return_value=test_df
    ) as mock_read_excel:
        result = read_financial_transactions("test.xlsx")

        # Проверяем вызов pd.read_excel
        mock_read_excel.assert_called_once()
        assert "openpyxl" in mock_read_excel.call_args[1].get("engine", "")  # Проверяем движок

        # Проверяем данные
        assert result == test_data


def test_file_not_found() -> None:
    """Тест ошибки, если файл не существует."""
    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            read_financial_transactions("missing_file.csv")


def test_unsupported_format() -> None:
    """Тест ошибки при неподдерживаемом формате."""
    with patch("pathlib.Path.exists", return_value=True):
        with pytest.raises(ValueError, match="Формат файла не поддерживается"):
            read_financial_transactions("invalid_file.txt")
