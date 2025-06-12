from collections import Counter
import re
from typing import List, Dict, Any


def count_transactions_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям

    Args:
        transactions: Список словарей с транзакциями
        categories: Список категорий для поиска

    Returns:
        Словарь {категория: количество_совпадений}
    """
    matched_categories: List[str] = []

    for tx in transactions:
        if "description" not in tx:
            continue

        description = tx["description"].lower()

        for category in categories:
            if re.search(re.escape(category.lower()), description, re.IGNORECASE):
                matched_categories.append(category)

    return dict(Counter(matched_categories))
