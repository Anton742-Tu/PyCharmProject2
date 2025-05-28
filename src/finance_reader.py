import pandas as pd
from typing import List, Dict, Union
from pathlib import Path


def read_financial_transactions(file_path: Union[str, Path]) -> List[Dict]:
    """
    Чтение финансовых операций из CSV или XLSX файла.

    Args:
        file_path: Путь к файлу (расширение .csv или .xlsx)

    Returns:
        Список словарей с финансовыми операциями

    Raises:
        ValueError: Если формат файла не поддерживается
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    if file_path.suffix.lower() == '.csv':
        # Чтение CSV с автоматическим определением разделителя
        df = pd.read_csv(file_path, delimiter=None, engine='python')
    elif file_path.suffix.lower() in ('.xlsx', '.xls'):
        # Чтение Excel файла
        df = pd.read_excel(file_path, engine='openpyxl')
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {file_path.suffix}")

    # Преобразование DataFrame в список словарей
    transactions = df.to_dict('records')

    # Очистка данных: удаление NaN значений и приведение к стандартному формату
    cleaned_transactions = []
    for trans in transactions:
        cleaned = {k: v for k, v in trans.items() if pd.notna(v)}
        cleaned_transactions.append(cleaned)

    return cleaned_transactions


def print_transactions(transactions: List[Dict]):
    """Печать списка финансовых операций в удобочитаемом формате."""
    for i, trans in enumerate(transactions, 1):
        print(f"Операция #{i}:")
        for key, value in trans.items():
            print(f"  {key}: {value}")
        print()
