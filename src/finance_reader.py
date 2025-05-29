from pathlib import Path
import pandas as pd


def get_transactions_path(filename: str) -> Path:
    """Возвращает абсолютный путь к файлу в папке transactions/."""
    # Поднимаемся на два уровня вверх из src/ (your_project/ -> transactions/)
    project_root = Path(__file__).parent.parent
    return project_root / "transactions" / filename


def read_financial_transactions(filename: str):
    """Читает CSV или XLSX файл из папки transactions/."""
    file_path = get_transactions_path(filename)

    if not file_path.exists():
        raise FileNotFoundError(f"Файл {filename} не найден в {file_path.parent}")

    if file_path.suffix == '.csv':
        return pd.read_csv(file_path).to_dict('records')
    elif file_path.suffix in ('.xlsx', '.xls'):
        return pd.read_excel(file_path, engine='openpyxl').to_dict('records')
    else:
        raise ValueError("Формат файла не поддерживается")
