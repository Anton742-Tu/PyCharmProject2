import pytest
from src.finance_reader import read_financial_transactions
import os
from pathlib import Path


def test_read_csv():
    data = read_financial_transactions("transactions.csv")
    assert len(data) > 0  # Проверка, что данные загружены


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_financial_transactions("nonexistent.csv")


def debug_file_location():
    print("Текущая рабочая папка:", os.getcwd())
    print("Содержимое папки transactions/:")
    transactions_dir = Path("transactions")
    if transactions_dir.exists():
        print(os.listdir(transactions_dir))
    else:
        print("Папка transactions/ не найдена!")

# Вставьте вызов в main() перед чтением файлов
debug_file_location()
