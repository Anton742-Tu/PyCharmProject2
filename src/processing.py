from datetime import datetime
from typing import List, Dict, Any


def filter_by_state(
        list_of_dicts: List[Dict[str, Any]],
        state: str = 'EXECUTED'
) -> List[Dict[str, Any]]:
    """
    Фильтрует словари по ключу 'state'.
    """
    assert isinstance(list_of_dicts, list), "list_of_dicts должен быть списком"
    assert isinstance(state, str), "state должен быть строкой"
    return [d for d in list_of_dicts if d.get('state') == state]


def sort_by_date(
        list_of_dicts: List[Dict[str, Any]],
        reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по дате (ключ 'date')
    """
    assert isinstance(list_of_dicts, list), "list_of_dicts должен быть списком"
    assert isinstance(reverse, bool), "reverse должен быть True или False"
    return sorted(list_of_dicts, key=lambda x: datetime.fromisoformat(x['date']), reverse=reverse)


# =========================================== ТЕСТЫ =================================================
def test_filter_by_state():
    # Тестовые данные
    test_data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "state": "EXECUTED"},
    ]

    # Проверяем фильтрацию
    filtered = filter_by_state(test_data, "EXECUTED")
    assert len(filtered) == 2, "Должно остаться 2 элемента"
    assert all(item["state"] == "EXECUTED" for item in filtered), "Все элементы должны быть EXECUTED"

    # Проверяем фильтрацию с дефолтным state="EXECUTED"
    filtered_default = filter_by_state(test_data)
    assert filtered == filtered_default, "Результаты должны совпадать"

def test_sort_by_date():
    # Тестовые данные
    test_data = [
        {"id": 1, "date": "2023-10-01T12:00:00"},
        {"id": 2, "date": "2023-09-15T08:30:00"},
        {"id": 3, "date": "2023-10-05T15:45:00"},
    ]

    # Проверяем сортировку по убыванию (новые сначала)
    sorted_desc = sort_by_date(test_data, reverse=True)
    assert sorted_desc[0]["id"] == 3, "Первым должен быть id=3 (самая поздняя дата)"
    assert sorted_desc[-1]["id"] == 2, "Последним должен быть id=2 (самая ранняя дата)"

    # Проверяем сортировку по возрастанию (старые сначала)
    sorted_asc = sort_by_date(test_data, reverse=False)
    assert sorted_asc[0]["id"] == 2, "Первым должен быть id=2 (самая ранняя дата)"
    assert sorted_asc[-1]["id"] == 3, "Последним должен быть id=3 (самая поздняя дата)"
