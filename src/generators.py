from typing import Iterator, Dict, Any


def filter_by_currency(transactions: list[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по коду валюты (например, "USD") и возвращает итератор.
    Валюта ищется в операции по пути: operationAmount -> currency -> code.
    """
    for transaction in transactions:
        # Проверяем вложенную структуру, избегая KeyError
        try:
            if transaction["operationAmount"]["currency"]["code"] == currency:
                yield transaction
        except KeyError:
            continue  # Пропускаем транзакции с некорректной структурой


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который возвращает описания транзакций по одной.
    """
    for transaction in transactions:
        yield transaction.get('description')


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате "XXXX XXXX XXXX XXXX".
    Диапазон: от start до end (включительно), где start ≥ 1 и end ≤ 9999999999999999.
    """
    if start < 1 or end > 9999999999999999:
        raise ValueError("Некорректный диапазон. Допустимые значения: 1 ≤ start ≤ end ≤ 9999999999999999")

    for number in range(start, end + 1):
        # Форматируем число в 16-значную строку с ведущими нулями и пробелами
        card_number = f"{number:016d}"
        yield f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}"
