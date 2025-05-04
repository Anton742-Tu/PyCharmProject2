# Учебный проект по PyThon:

## Описание:
Изучаем функционал 'PyCharm' добавляем новые модули и функции, работаем в (Github.com).

## Установка:
- Установить зависимости.
```
pip install -r requirements.txt
```
- Установка тестировщика
```
pip install pytest
```

## Примеры использования функции:
### Модуль 'widget.py'
 - Катры с 15-ю цифрами:
 - print(mask_account_card(American Express 123456789012345))
Вывод: American Express 1234 56**** **345
 - Другие карты с 16 цифрами:
 - print(mask_account_card("Visa 1234567890123456"))
Вывод: "Visa 1234 56** **** 3456"

### Пример срабатывания 'assert' в модуле 'processing.py'
 - Вызовет AssertionError: 'list_of_dicts должен быть списком'
filter_by_state(None, "EXECUTED")  

 - Вызовет AssertionError: 'state должен быть строкой'
filter_by_state([{"state": "EXECUTED"}], 123)  

 - Вызовет AssertionError: 'list_of_dicts должен быть списком'
sort_by_date('not a list')  

 - Вызовет AssertionError: 'reverse должен быть True или False'
sort_by_date([{"date": "2023-01-01"}], reverse="yes")

## Документация:
Тестирование проводиться через команду 'Pytest' или 'python main.py'
В процессе выполнения тестов, показана работа функций из модуля
'masks' и 'widget'

## Тестирование:
 - Тестирование с помощью 'assert', модуля 'widget.py'
 - Тестирование с помощью 'assert', модуля 'processing.py'
