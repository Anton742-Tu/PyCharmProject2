import unittest
from src.transaction_stats import count_transactions_by_category


class TestTransactionStats(unittest.TestCase):
    def setUp(self) -> None:
        """Подготовка тестовых данных"""
        self.sample_transactions = [
            {"amount": 100, "description": "Покупка в магазине ABC"},
            {"amount": 200, "description": "Кафе 'Кофейня'"},
            {"amount": 50, "description": "Оплата интернета"},
            {"amount": 300, "description": "Продуктовый магазин"},
            {"amount": 150, "description": "Перевод другу"},
        ]
        self.base_categories = ["магазин", "кафе", "интернет", "перевод"]

    def test_basic_functionality(self) -> None:
        """Тест базовой функциональности"""
        result = count_transactions_by_category(
            self.sample_transactions,
            self.base_categories
        )
        expected = {
            "магазин": 2,
            "кафе": 1,
            "интернет": 1,
            "перевод": 1
        }
        self.assertEqual(result, expected)

    def test_case_insensitivity(self) -> None:
        """Тест регистронезависимого поиска"""
        result = count_transactions_by_category(
            self.sample_transactions,
            ["МАГАЗИН", "КаФе"]
        )
        expected = {
            "МАГАЗИН": 2,
            "КаФе": 1
        }
        self.assertEqual(result, expected)

    def test_empty_categories(self) -> None:
        """Тест с пустым списком категорий"""
        result = count_transactions_by_category(
            self.sample_transactions,
            []
        )
        self.assertEqual(result, {})

    def test_special_chars_in_categories(self) -> None:
        """Тест с спецсимволами в категориях"""
        transactions = [
            {"amount": 100, "description": "Покупка в магазине (ABC)"},
            {"amount": 200, "description": "Кафе + кофейня"},
        ]
        result = count_transactions_by_category(
            transactions,
            ["(ABC)", "+ кофейня"]
        )
        expected = {
            "(ABC)": 1,
            "+ кофейня": 1
        }
        self.assertEqual(result, expected)

    def test_performance_on_large_data(self) -> None:
        """Тест производительности на большом наборе данных"""
        # Генерация 10,000 тестовых транзакций
        large_transactions = [
            {"amount": i, "description": f"Transaction {i}"}
            for i in range(10000)
        ]
        large_transactions.extend([
            {"amount": 100, "description": "Покупка в магазине"},
            {"amount": 200, "description": "Оплата интернета"},
        ])

        categories = ["магазин", "интернет"]

        import time
        start_time = time.time()
        result = count_transactions_by_category(
            large_transactions,
            categories
        )
        execution_time = time.time() - start_time

        self.assertEqual(result, {"магазин": 1, "интернет": 1})
        self.assertLess(execution_time, 1.0, "Функция работает слишком медленно")


if __name__ == "__main__":
    unittest.main()
