from dataclasses import dataclass
from typing import Literal, TypedDict
import requests

# Определяем типы для валют
Currency = Literal["RUB", "USD", "EUR"]


# Определяем структуру транзакции с помощью TypedDict
class Transaction(TypedDict):
    amount: float | str
    currency: Currency


# Или через dataclass (альтернативный вариант)
@dataclass
class TransactionDC:
    amount: float | str
    currency: Currency


# Определяем тип для ответа API курсов валют
class ExchangeRates(TypedDict):
    rates: dict[str, float]
    base: str
    date: str


def get_amount_in_rub(transaction: Transaction | TransactionDC) -> float:
    """
    Возвращает сумму транзакции в рублях.
    Поддерживает конвертацию из USD и EUR через внешний API.

    Args:
        transaction: Словарь или dataclass с данными транзакции, должен содержать:
            - amount (float | str): сумма
            - currency (Currency): валюта ('RUB', 'USD', 'EUR')

    Returns:
        Сумма в рублях (float)

    Raises:
        ValueError: Если передана неподдерживаемая валюта
        requests.RequestException: Если ошибка при запросе к API
        KeyError: Если в ответе API нет нужных курсов валют
    """
    currency = transaction['currency'].upper() if isinstance(transaction, dict) else transaction.currency.upper()
    amount = float(transaction['amount'] if isinstance(transaction, dict) else transaction.amount)

    if currency == "RUB":
        return amount

    try:
        response = requests.get("https://apilayer.com/exchangerates_data-api", timeout=5)
        response.raise_for_status()
        rates_data: ExchangeRates = response.json()
        rates = rates_data["rates"]
    except requests.RequestException as e:
        raise requests.RequestException(f"Ошибка при получении курсов валют: {e}")
    except KeyError as e:
        raise KeyError(f"Неверный формат ответа от API: отсутствует ключ {e}")

    conversion_rates = {
        "USD": 1 / rates["USD"],
        "EUR": 1 / rates["EUR"],
    }

    if currency not in conversion_rates:
        raise ValueError(f"Неподдерживаемая валюта: {currency}")

    result = amount * conversion_rates[currency]
    return round(result, 2)
