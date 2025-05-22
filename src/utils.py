import json
from typing import Union, Dict, List, Any


def read_transactions_from_json(file_path: str) -> Union[Dict[str, Any], List[Any]]:
    """
    Читает JSON-файла и возвращает список транзакций

    Аргументы:
        file_path(str): Путь к JSON-файлу с транзакциями

    Возвращает:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях
        или пустой список в случае ошибок
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Если данные не список или файл пустой
            if not isinstance(data, list):
                return []

            return data

    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except Exception:
        # На всякий случай перехватываем все остальные исключения
        return []
