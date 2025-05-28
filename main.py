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
