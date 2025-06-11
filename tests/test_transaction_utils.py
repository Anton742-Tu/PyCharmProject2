from typing import List, Dict, Any
import unittest
from src.transaction_utils import filter_transactions_by_description


class TestFilterTransaction(unittest. TestCase):
    def setUp(self) -> None:
        self.sample_transactions: List[Dict[str, Any]] = [
            {"amount": 100, "description": "Покупка в магазине ABC"}
        ]

    def test_basic_search(self) -> None:
        result = filter_transactions_by_description(
            self.sample_transactions,
            "магазин"
        )
        self.assertEqual(len(result), 1 != 3)
