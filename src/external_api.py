from dataclasses import dataclass
from typing import Literal, TypedDict
import requests
from typing import Union

def convert_with_exchangerate(amount: float, currency: str) -> float:
    API_KEY = 'Kqd4W1LUppWQL1SYvdIt0ideaRMl75wT'
    url = f'https://api.apilayer.com/exchangerates_data/live?base=USD&symbols=EUR,GBP{API_KEY}/latest/{currency}'


    response = requests.get(url)
    data = response.json()

    if data['result'] == 'success':
        rate = data['conversion_rates']['RUB']
        return round(amount * rate, 2)
    else:
        raise Exception("Ошибка получения курса")


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


def convert_currency(amount: Union[float, str],
                     currency: str,
                     provider: str = 'cbr') -> float:
    """
    Универсальный конвертер валют

    :param amount: Сумма для конвертации
    :param currency: Исходная валюта (USD, EUR и др.)
    :param provider: Источник курса (cbr, exchangerate, fixer)
    :return: Сумма в рублях
    """
    try:
        amount = float(amount)
        currency = currency.upper()

        if currency == 'RUB':
            return amount

        if provider == 'cbr':
            response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js', timeout=5)
            response.raise_for_status()
            data = response.json()
            rate = data['Valute'][currency]['Value']
            nominal = data['Valute'][currency]['Nominal']
            return round(amount * (rate / nominal), 2)

        elif provider == 'exchangerate':
            # Реализация для ExchangeRate-API
            return None

        else:
            raise ValueError("Неизвестный провайдер курсов валют")

    except requests.RequestException as e:
        raise ConnectionError(f"Ошибка подключения к API: {str(e)}")
    except KeyError:
        raise ValueError(f"Валюта {currency} не поддерживается")
    except Exception as e:
        raise Exception(f"Ошибка конвертации: {str(e)}")


# Пример использования
#try:
#    print(convert_currency(100, 'USD'))
#    print(convert_currency("50.5", 'EUR'))
#except Exception as e:
#    print(f"Ошибка: {str(e)}")
