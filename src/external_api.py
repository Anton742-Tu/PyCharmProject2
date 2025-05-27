import os
import requests
from typing import Dict, Union, cast
from dotenv import load_dotenv

load_dotenv()


def get_amount_in_rub(transaction: Dict[str, Union[str, float, int]]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с ключами 'amount' (str | float | int) и 'currency' (str).

    Returns:
        Сумма в рублях (float).

    Raises:
        ValueError: Если API ключ отсутствует или курс валюты не получен.
    """
    # Явное приведение amount к float
    amount_str = transaction.get("amount")
    if amount_str is None:
        amount = 0.0
    else:
        amount = float(amount_str)  # Гарантированно float

    currency = str(transaction.get("currency", "RUB")).upper()

    if currency == "RUB":
        return amount

    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        raise ValueError("API ключ не найден в .env")

    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB"

    try:
        response = requests.get(url, headers={"apikey": API_KEY}, timeout=10)
        response.raise_for_status()

        # Аннотация типа для response.json()
        data = cast(Dict[str, Dict[str, float]], response.json())

        rate = data["rates"]["RUB"]  # Теперь mypy знает, что это float
        return amount * rate

    except Exception as e:
        raise ValueError(f"Ошибка конвертации: {e}")
