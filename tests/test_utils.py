from typing import Dict, Union
from unittest.mock import patch, Mock
from src.external_api import get_amount_in_rub


def test_usd_transaction() -> None:
    transaction: Dict[str, Union[str, float]] = {'amount': '100', 'currency': 'USD'}

    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {'rates': {'RUB': 75.0}}
        mock_get.return_value = mock_response

        result = get_amount_in_rub(transaction)
        assert result == 7500.0
