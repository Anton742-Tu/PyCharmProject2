import os
import requests
from dotenv import load_dotenv
from typing import Dict, Union, Optional


# Загружаем переменные из .env
load_dotenv()


def get_amount_in_rub(_transaction: Dict[str, Union[str, float]]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
         _transaction: Словарь с ключами 'amount' (str | float) и 'currency' (str).
    Returns:
         Сумма в рублях (float).
    Raises:
         ValueError: Если API ключ отсутствует или курс валюты не получен.
    """
    amount = float(_transaction.get('amount', 0))
    currency = _transaction.get('currency', 'RUB').upper()

    if currency == 'RUB':
        return amount

    API_KEY: Optional[str] = os.getenv('API_KEY')
    if not API_KEY:
        raise ValueError("API ключ не найден в переменных окружения")

    URL = f'https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB'

    try:
        response: requests.Response = requests.get(
            URL,
            headers={'apikey': API_KEY},
            timeout=10
        )
        response.raise_for_status()
        data: Dict = response.json()

        if 'rates' not in data or 'RUB' not in data['rates']:
            raise ValueError(f"Не удалось получить курс {currency} к RUB")

        rate: float = data['rates']['RUB']
        return amount * rate

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Ошибка при запросе к API: {e}")


# Пример использования (для тестов)
if __name__ == "__main__":
    transaction = {'amount': '100', 'currency': 'USD'}
    print(get_amount_in_rub(transaction))
