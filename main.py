from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date
from tests.test_processing import test_filter_by_state, test_sort_by_date
from tests.test_main import test_mask_account_card, test_get_date
from src.utils import read_transactions_from_json, write_transactions_to_json
from typing import List, Dict, Any


# Примеры использования: 'masks', 'widget'
if __name__ == "__main__":
    print("<<< Примеры использования функций >>>")
    print(get_mask_card_number(1234565409877654))
    print(get_mask_account(3456))
    print(mask_account_card("American Express 123456789087543"))
    print(get_date("2024-03-11T02:26:18.671407"))


# Запуск тестов 'widget'
if __name__ == "__main__":
    test_mask_account_card()
    test_get_date()
    print("- Тесты модуля 'widget.py'\n Прошли успешно!")


# Запуск тестов 'processing'
if __name__ == "__main__":
    test_filter_by_state()
    test_sort_by_date()
    print("- Тесты модуля 'processing.py'\n Прошли успешно!")


# Пример использования 'utils'
if __name__ == "__main__":
    # Тест чтения
    transactions: List[Dict[str, Any]] = read_transactions_from_json("data/transactions.json")
    print(f"Прочитано транзакций: {len(transactions)}")

    # Тест записи
    success: bool = write_transactions_to_json(transactions, "data/transactions_copy.json")
    print(f"Запись выполнена: {'успешно' if success else 'с ошибкой'}")

import os
from pathlib import Path
from typing import List, Dict, Any, TypeVar
from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date
from src.decorators import log, write_log
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
from src.finance_reader import get_transactions_path, read_financial_transactions
from src.utils import read_transactions_from_json, write_transactions_to_json
from src.external_api import get_amount_in_rub
from src.transaction_utils import filter_transactions_by_description
from src.transaction_stats import count_transactions_by_category

T = TypeVar("T")


def print_transaction(transaction: Dict[str, Any]) -> None:
    """Печатает информацию о транзакции с использованием всех необходимых функций"""
    date = get_date(transaction.get("date", ""))
    description = transaction.get("description", "")

    # Используем функции маскирования напрямую
    from_: str = ""
    if transaction.get("from"):
        if "счет" in str(transaction["from"]).lower():
            from_ = f"Счет {get_mask_account(str(transaction['from']).split()[-1])}"
        else:
            card_num = "".join(filter(str.isdigit, str(transaction["from"]).split()[-1]))
            from_ = f"{' '.join(str(transaction['from']).split()[:-1])} {get_mask_card_number(card_num)}"

    to_account = str(transaction.get("to", ""))
    if "счет" in to_account.lower():
        to = f"Счет {get_mask_account(to_account.split()[-1])}"
    else:
        card_num = "".join(filter(str.isdigit, to_account.split()[-1]))
        to = f"{' '.join(to_account.split()[:-1])} {get_mask_card_number(card_num)}"

    amount = transaction.get("amount", 0)
    currency = transaction.get("currency", "RUB")

    if currency != "RUB":
        try:
            amount_rub = get_amount_in_rub(transaction)
            amount_str = f"{amount} {currency} (~{amount_rub:.2f} руб.)"
        except ValueError:
            amount_str = f"{amount} {currency} (не удалось конвертировать)"
    else:
        amount_str = f"{amount} руб."

    print(f"{date} {description}")
    if from_:
        print(f"{from_} -> {to}")
    else:
        print(f"{to}")
    print(f"Сумма: {amount_str}\n")


def generate_sample_card_numbers() -> None:
    """Демонстрация работы генератора номеров карт"""
    print("\nПример работы генератора номеров карт:")
    for i, num in enumerate(card_number_generator(1, 5), 1):
        print(f"{i}. {num}")


def show_transaction_descriptions(transactions: List[Dict[str, Any]]) -> None:
    """Демонстрация работы генератора описаний транзакций"""
    print("\nВсе описания транзакций:")
    for i, desc in enumerate(transaction_descriptions(transactions), 1):
        print(f"{i}. {desc}")


def show_category_stats(transactions: List[Dict[str, Any]]) -> None:
    """Демонстрация статистики по категориям"""
    categories = list(set(t.get("category") for t in transactions if t.get("category")))
    valid_categories = [str(cat) for cat in categories if cat is not None]
    if valid_categories:
        stats = count_transactions_by_category(transactions, valid_categories)
        print("\nСтатистика по категориям операций:")
        for cat, count in stats.items():
            print(f"- {cat}: {count} операций")
    else:
        print("\nВ транзакциях отсутствует информация о категориях")


@log  # type: ignore
def write_operation_log(message: str) -> None:
    """Демонстрация работы логгера"""
    write_log(f"Лог операции: {message}")


def get_user_choice(prompt: str, valid_choices: List[str]) -> str:
    """Получает выбор пользователя с валидацией"""
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        print(f"Ошибка: допустимые варианты - {', '.join(valid_choices)}")


def get_full_path(file_type: str, filename: str) -> Path:
    """Возвращает абсолютный путь к файлу"""
    project_root = Path(__file__).parent.parent
    if file_type == "1":  # JSON
        return project_root / "data" / filename
    else:  # CSV или XLSX
        return project_root / "transactions" / filename


def check_file(filepath: Path) -> bool:
    """Проверяет существование и читаемость файла"""
    if not filepath.exists():
        print(f"Ошибка: файл {filepath} не найден")
        return False
    if filepath.stat().st_size == 0:
        print(f"Ошибка: файл {filepath} пуст")
        return False
    return True


@log  # type: ignore
def main() -> None:
    print("Добро пожаловать в программу работы с банковскими транзакциями!")
    print("Выберите источник данных:")
    print("1. JSON-файл")
    print("2. CSV-файл")
    print("3. Excel-файл (XLSX)")

    file_type = get_user_choice("Ваш выбор (1-3): ", ["1", "2", "3"])

    default_files = {"1": "transactions.json", "2": "transactions.csv", "3": "Transactions_excel.xlsx"}

    filename = (
        input(f"Введите имя файла (по умолчанию {default_files[file_type]}): ").strip() or default_files[file_type]
    )

    file_path = get_full_path(file_type, filename)

    if not check_file(file_path):
        print("\nПроверьте следующее:")
        print(f"1. Файл должен находиться в папке {'data' if file_type == '1' else 'transactions'}")
        print(f"2. Текущий рабочий каталог: {os.getcwd()}")
        return

    transactions: List[Dict[str, Any]] = []
    try:
        if file_type == "1":
            transactions = read_transactions_from_json(str(file_path))
        else:
            transactions = read_financial_transactions(str(file_path))

        print(f"\nУспешно загружено транзакций: {len(transactions)}")

    except Exception as e:
        print(f"\nОшибка при чтении файла: {type(e).__name__}: {e}")
        return

    if not transactions:
        print("Нет данных для обработки")
        return

    # Фильтрация по статусу
    while True:
        state = input("\nФильтр по статусу (EXECUTED, CANCELED, PENDING): ").strip().upper()

        if state in ["EXECUTED", "CANCELED", "PENDING"]:
            filtered_transactions = filter_by_state(transactions, state)
            print(f"Найдено операций: {len(filtered_transactions)}")
            break
        print("Некорректный статус операции!")

    # Сортировка
    if get_user_choice("\nСортировать по дате? (да/нет): ", ["да", "нет"]) == "да":
        reverse = (
            get_user_choice("Порядок сортировки (возрастанию/убыванию): ", ["возрастанию", "убыванию"]) == "убыванию"
        )
        filtered_transactions = sort_by_date(filtered_transactions, reverse)

    # Дополнительные фильтры
    if get_user_choice("\nТолько рублевые транзакции? (да/нет): ", ["да", "нет"]) == "да":
        filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))

    if get_user_choice("\nФильтровать по описанию? (да/нет): ", ["да", "нет"]) == "да":
        query = input("Введите текст для поиска: ").strip()
        filtered_transactions = filter_transactions_by_description(filtered_transactions, query)

    # Вывод результатов
    print("\nРезультаты:")
    if not filtered_transactions:
        print("Нет транзакций, соответствующих условиям")
    else:
        print(f"Всего операций: {len(filtered_transactions)}\n")
        for t in filtered_transactions:
            print_transaction(t)

        # Демонстрация всех функций
        generate_sample_card_numbers()
        show_transaction_descriptions(filtered_transactions)
        show_category_stats(filtered_transactions)
        write_operation_log("Программа успешно завершила работу")

        # Сохранение результатов
        if get_user_choice("\nСохранить результаты? (да/нет): ", ["да", "нет"]) == "да":
            output_file = input("Имя файла для сохранения (без расширения): ").strip() + ".json"
            try:
                write_transactions_to_json(filtered_transactions, str(get_full_path("1", output_file)))
                print(f"Данные сохранены в {output_file}")
            except Exception as e:
                print(f"Ошибка при сохранении: {e}")


if __name__ == "__main__":
    main()
