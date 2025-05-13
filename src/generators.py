from typing import List, Dict, Any, Iterator


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте.
    """
    if not isinstance(transactions, list):
        raise TypeError("transactions должен быть списком")
    if not isinstance(currency, str):
        raise TypeError("currency должен быть строкой")
    if len(currency) != 3:
        raise ValueError("currency должен быть строкой из 3 символов")

    for transaction in transactions:
        if not isinstance(transaction, dict):
            continue  # Пропускаем некорректные элементы

        try:
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
                yield transaction
        except AttributeError:
            continue


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который возвращает описания транзакций (только строки!).
    Пропускает транзакции без описания или с описанием не строкового типа.
    """
    for transaction in transactions:
        description = transaction.get("description")
        if isinstance(description, str):  # Проверяем, что описание это строка
            yield description


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате "XXXX XXXX XXXX XXXX".
    Диапазон: от start до end (включительно), где start ≥ 1 и end ≤ 9999999999999999.
    """
    if start > end:
        raise ValueError("Start must be less than or equal to end")
    if start < 1 or end > 9999999999999999:
        raise ValueError("Numbers must be between 1 and 9999999999999999")

    for number in range(start, end + 1):
        # Форматируем число в 16-значную строку с ведущими нулями и пробелами
        card_number = f"{number:016d}"
        yield f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}"
