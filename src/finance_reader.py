from pathlib import Path
import pandas as pd
from typing import List, Dict, Any, Hashable
from typing import cast


def get_transactions_path(filename: str) -> Path:
    """Возвращает абсолютный путь к файлу в папке transactions/."""
    project_root = Path(__file__).parent.parent
    return project_root / "transactions" / filename


def read_financial_transactions(filename: str) -> List[Dict[str, Any]]:
    """
    Читает CSV или XLSX файл из папки transactions/.

    Args:
        filename: Имя файла с расширением (.csv, .xlsx, .xls)

    Returns:
        Список словарей, где ключи - строки (названия колонок),
        значения - любые данные из таблицы
    """
    file_path = get_transactions_path(filename)

    if not file_path.exists():
        raise FileNotFoundError(f"Файл {filename} не найден в {file_path.parent}")

    try:
        if file_path.suffix == '.csv':
            data = pd.read_csv(file_path)
        elif file_path.suffix in ('.xlsx', '.xls'):
            data = pd.read_excel(file_path, engine='openpyxl')
        else:
            raise ValueError("Формат файла не поддерживается")

        # Явное приведение типов для mypy
        return cast(List[Dict[str, Any]], data.to_dict('records'))

    except pd.errors.EmptyDataError:
        raise ValueError("Файл не содержит данных")
    except Exception as e:
        raise ValueError(f"Ошибка при чтении файла: {str(e)}")
