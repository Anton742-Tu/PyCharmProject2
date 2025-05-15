from src.processing import filter_by_state, sort_by_date


def test_filter_by_state() -> None:
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


def test_sort_by_date() -> None:
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
