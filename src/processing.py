from datetime import datetime
from typing import List, Dict, Any


def filter_by_state(
        list_of_dicts: List[Dict[str, Any]],
        state: str = 'EXECUTED'
) -> List[Dict[str, Any]]:
    """
    Фильтр список словарей, оставляя только те, у которых ключ 'state' соответствует заданному значению.
    :param list_of_dicts: Список словарей для фильтрации.
    :param state: Значение ключа 'state' для фильтрации.
    :return: Новый список словарей.
    """
    return [d for d in list_of_dicts if d.get('state') == state]


def sort_by_date(
        list_of_dicts: List[Dict[str, Any]],
        reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по дате (ключ 'date')
    :param list_of_dicts: Список словарей для сортировки.
    :param reverse: Если True (по умолчанию), сортирует по убыванию (новые сначала)
                    Если False, то по возрастанию.
    :return: Новый отсортированный список словарей.
    """
    return sorted(
        list_of_dicts,
        key=lambda x: datetime.fromisoformat(x['date']),
        reverse=reverse
    )
