# Учебный проект по PyThon:

## *Описание:*
Создаём проект для банковского обслуживания клиентов.
(Изучаем функционал 'PyCharm' добавляем новые модули и функции, работаем в (Github.com)).

## *Установка:*
- Установить зависимости.
```
pip install -r requirements.txt
```
- Установка тестировщика
```
pip install pytest
```

## *Примеры использования функций:*
## *Модуль 'widget.py'*
### [Функция mask_account_card:](https://write.geeksforgeeks.org/)
 - Катры с 15-ю цифрами:
 - print(mask_account_card(American Express 123456789012345))
Вывод: American Express 1234 56**** **345
 - Другие карты с 16 цифрами:
 - print(mask_account_card("Visa 1234567890123456"))
Вывод: "Visa 1234 56** **** 3456"

## *Модуль 'generators.py'*
### [Функция filter_by_currency:](https://write.geeksforgeeks.org/)
```usd_transactions = filter_by_currency(transactions, "USD")```

 - Получаем две транзакции через next()
```
print(next(usd_transactions))  # Первая USD-транзакция
print(next(usd_transactions))  # Вторая USD-транзакция
```
### [Функция transaction_description:](https://write.geeksforgeeks.org/)
```
transactions = [
    {"id": 1, "description": "Перевод организации"},
    {"id": 2, "description": None},                  # Пропустится
    {"id": 3, "description": "Покупка валюты"},
    {"id": 4, "description": 12345},                # Пропустится (не строка)
    {"id": 5},                                      # Пропустится (нет ключа)
]
```

 - Получаем только строковые описания
```
for desc in transaction_descriptions(transactions):
    print(desc)
```

### [Функция card_number_generator:](https://write.geeksforgeeks.org/)
 - Генерация номеров от "0000 0000 0000 0001" до "0000 0000 0000 0005"
```
card_gen = card_number_generator(1, 5)
for _ in range(5):
    print(next(card_gen))
```
## *Модуль 'decorators.py'*
### [Функция filename:](https://write.geeksforgeeks.org/)
```
@log('operations.log')
def divide(a, b):
    """Простая функция деления"""
    return a / b

# Успешный вызов
divide(10, 2)

# Вызов с ошибкой
divide(10, 0)
```
## *Примеры использования тест-кейсов:*
### [Вывод тестов для функции 'filter_by_currency'](https://write.geeksforgeeks.org/)
```
test_filter_by_currency.py::test_filter_by_currency[USD-expected_ids0] PASSED
test_filter_by_currency.py::test_filter_by_currency[EUR-expected_ids1] PASSED
test_filter_by_currency.py::test_filter_by_currency[RUB-expected_ids2] PASSED
test_filter_by_currency.py::test_filter_by_currency[GBP-expected_ids3] PASSED
test_filter_by_currency.py::test_filter_by_currency_empty_input PASSED
test_filter_by_currency.py::test_filter_by_currency_invalid_structure PASSED
```
### [Вывод тестов для функции 'transaction_descriptions '](https://write.geeksforgeeks.org/)
```
test_transaction_descriptions.py::test_transaction_descriptions_valid PASSED
test_transaction_descriptions.py::test_transaction_descriptions_empty_list PASSED
test_transaction_descriptions.py::test_transaction_descriptions_no_description PASSED
test_transaction_descriptions.py::test_transaction_descriptions_parametrized[Оплата налогов-expected0] PASSED
test_transaction_descriptions.py::test_transaction_descriptions_parametrized[None-expected1] PASSED
test_transaction_descriptions.py::test_transaction_descriptions_parametrized[123-expected2] PASSED
test_transaction_descriptions.py::test_transaction_descriptions_parametrized[-expected3] PASSED
```
### [Вывод тестов для функции 'card_number_generator'](https://write.geeksforgeeks.org/)
```
test_card_number_generator.py::test_card_number_generator_range[1-3-expected_numbers0] PASSED
test_card_number_generator.py::test_card_number_generator_range[9999-10001-expected_numbers1] PASSED
test_card_number_generator.py::test_card_number_generator_format PASSED
test_card_number_generator.py::test_card_number_generator_invalid_range PASSED
test_card_number_generator.py::test_card_number_generator_edge_cases PASSED
```
### [Пример срабатывания 'assert' в модуле 'processing.py'](https://write.geeksforgeeks.org/)
 - Вызовет AssertionError: 'list_of_dicts должен быть списком'
```
filter_by_state(None, "EXECUTED")  
```
 - Вызовет AssertionError: 'state должен быть строкой'
```
filter_by_state([{"state": "EXECUTED"}], 123)  
```
 - Вызовет AssertionError: 'list_of_dicts должен быть списком'
```
sort_by_date('not a list')  
```
 - Вызовет AssertionError: 'reverse должен быть True или False'
```
sort_by_date([{"date": "2023-01-01"}], reverse="yes")
```
## *Пример использования JSON-файла и конвертации валют:*
### [Модуль 'utils'](https://write.geeksforgeeks.org/)
```
transactions = read_transactions_from_json('transactions.json')

if transactions:
    print(f"Найдено {len(transactions)} транзакций:")
    for tx in transactions:
        print(f"- {tx.get('date', 'нет даты')}: {tx.get('amount', 0)}")
else:
    print("Транзакции не найдены или файл поврежден")
```
### [Модуль 'external_api'](https://write.geeksforgeeks.org/)
```
transaction1 = {'amount': '100', 'currency': 'RUB'}
transaction2 = {'amount': '50', 'currency': 'USD'}
transaction3 = {'amount': '70', 'currency': 'EUR'}

print(get_amount_in_rub(transaction1))  # 100.0
print(get_amount_in_rub(transaction2))  # Конвертирует USD в RUB по текущему курсу
print(get_amount_in_rub(transaction3))  # Конвертирует EUR в RUB по текущему курсу
```
## *Документация:*
Тестирование проводиться через команду 'Pytest' или 'python main.py'
В процессе выполнения тестов, показана работа функций из модуля
'masks' и 'widget'
## *Инструкция:*
Перед запуском проекта:
1. Скопируйте .env.example в .env
2. Заполните .env реальными значениями
## *Тестирование:*
 - Тестирование с помощью 'assert', модуля 'widget.py'
 - Тестирование с помощью 'assert', модуля 'processing.py'
 - Также добавили Фикстуры, парамитризационные данные в другие модули.
