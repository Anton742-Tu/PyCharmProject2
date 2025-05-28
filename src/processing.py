from datetime import datetime
from typing import List, Dict, Any


def filter_by_state(list_of_dicts: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует словари по ключу 'state'.
    """
    return [d for d in list_of_dicts if d.get("state") == state]


def sort_by_date(list_of_dicts: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по дате (ключ 'date')
    """
    return sorted(list_of_dicts, key=lambda x: datetime.fromisoformat(x["date"]), reverse=reverse)
