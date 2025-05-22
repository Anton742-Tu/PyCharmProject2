from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date
from tests.test_processing import test_filter_by_state, test_sort_by_date
from tests.test_main import test_mask_account_card, test_get_date


if __name__ == "__main__":
    print("<<< Примеры использования функций >>>")
    print(get_mask_card_number(1234565409877654))
    print(get_mask_account(3456))
    print(mask_account_card("American Express 123456789087543"))
    print(get_date("2024-03-11T02:26:18.671407"))


if __name__ == "__main__":
    test_mask_account_card()
    test_get_date()
    print("- Тесты модуля 'widget.py'\n Прошли успешно!")


# Запуск тестов
if __name__ == "__main__":
    test_filter_by_state()
    test_sort_by_date()
    print("- Тесты модуля 'processing.py'\n Прошли успешно!")


if __name__ == "__main__":
    # Вариант с TypedDict
    transaction1: Transaction = {"amount": "100", "currency": "RUB"}
    transaction2: Transaction = {"amount": 50, "currency": "USD"}

    # Вариант с dataclass
    transaction3 = TransactionDC(amount="70", currency="EUR")

    print(get_amount_in_rub(transaction1))  # 100.0
    print(get_amount_in_rub(transaction2))  # Конвертирует USD в RUB
    print(get_amount_in_rub(transaction3))  # Конвертирует EUR в RUB
