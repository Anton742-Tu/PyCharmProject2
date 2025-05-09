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

## *Примеры использования функции:*
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
usd_transactions = filter_by_currency(transactions, "USD")

 - Получаем две транзакции через next()
print(next(usd_transactions))  # Первая USD-транзакция
print(next(usd_transactions))  # Вторая USD-транзакция

### [Функция transaction_description:](https://write.geeksforgeeks.org/)
 - Создаём генератор
descriptions = transaction_descriptions(transactions)

 - Получаем описания по одному через next()
print(next(descriptions))  # "Перевод организации"
print(next(descriptions))  # "Перевод со счета на счет"
print(next(descriptions))  # "Покупка валюты"

 - Или обходим в цикле
for desc in transaction_descriptions(transactions):
 - print(desc)

### [Функция card_number_generator:](https://write.geeksforgeeks.org/)
 - Генерация номеров от "0000 0000 0000 0001" до "0000 0000 0000 0005"

card_gen = card_number_generator(1, 5)
for _ in range(5):
    print(next(card_gen))

### [Пример срабатывания 'assert' в модуле 'processing.py'](https://write.geeksforgeeks.org/)
 - Вызовет AssertionError: 'list_of_dicts должен быть списком'
filter_by_state(None, "EXECUTED")  

 - Вызовет AssertionError: 'state должен быть строкой'
filter_by_state([{"state": "EXECUTED"}], 123)  

 - Вызовет AssertionError: 'list_of_dicts должен быть списком'
sort_by_date('not a list')  

 - Вызовет AssertionError: 'reverse должен быть True или False'
sort_by_date([{"date": "2023-01-01"}], reverse="yes")

## *Документация:*
Тестирование проводиться через команду 'Pytest' или 'python main.py'
В процессе выполнения тестов, показана работа функций из модуля
'masks' и 'widget'

## *Тестирование:*
 - Тестирование с помощью 'assert', модуля 'widget.py'
 - Тестирование с помощью 'assert', модуля 'processing.py'
