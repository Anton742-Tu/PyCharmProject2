import re
from typing import List, Dict, Any


def filter_transaction_by_description(transactions: List[Dict[str, Any]], search_query: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по строке поиска в описании

    Args:
         transactions: Список словарей с транзакциями
         search_query: Строка для поиска (регистрозависимо)

    Returns:
        Отфильтрованный список транзакций
    """
    if not search_query:
        return transactions.copy()

    pattern = re.compile(re.escape(search_query), re.IGNORECASE)
    return [tx for tx in transactions if "description" in tx and pattern.search(tx["description"])]
