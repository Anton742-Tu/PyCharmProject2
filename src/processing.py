def filter_by_state(list_of_dicts, state='EXECUTED'):
    """
    Фильтр список словарей, оставляя только те, у которых ключ 'state' соответствует заданному значению.
    :param list_of_dicts: Список словарей для фильтрации.
    :param state: Значение ключа 'state' для фильтрации.
    :return: Новый список словарей.
    """
    return [d for d in list_of_dicts if d.get ('state') == state]


from datetime import datetime

def sort_by_date(list_of_dicts, reverse=True):
    """
    Сортирует список словарей по дате (ключ 'date')
    :param list_of_dicts: Список словарей для сортировки.
    :param reverse: Если True (по умолчанию), сортирует по убыванию (новые сначала)
                    Если False, сортирует по возрастанию (старые сначала).
    :return: Новый отсортированный список словарей.
    """
    return sorted(
        list_of_dicts,
        key=lambda x: datetime.fromisoformat(x['date']),
        reverse=reverse
    )
