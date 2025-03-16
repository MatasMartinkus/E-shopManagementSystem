import unittest
from unittest.mock import MagicMock, patch
from src.controllers.financial_controller import FinancialController

class TestFinancialController(unittest.TestCase):
    def setUp(self):
        self.financial_controller = FinancialController()

    @patch('src.controllers.financial_controller.get_db')
    def test_add_transaction(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        transaction = self.financial_controller.add_transaction(
            transaction_date="2023-01-01",
            amount=100.0,
            transaction_type="Income",
            recipient="Recipient",
            sender="Sender"
        )
        self.assertIsNotNone(transaction)
        mock_db.add.assert_called()
        mock_db.commit.assert_called()

    @patch('src.controllers.financial_controller.get_db')
    def test_edit_transaction(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(id=1)
        transaction = self.financial_controller.edit_transaction(
            transaction_id=1,
            amount=200.0
        )
        self.assertIsNotNone(transaction)
        mock_db.commit.assert_called()

    @patch('src.controllers.financial_controller.get_db')
    def test_delete_transaction(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(id=1)
        self.financial_controller.delete_transaction(1)
        mock_db.delete.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()