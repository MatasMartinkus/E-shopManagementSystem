import unittest
from unittest.mock import MagicMock, patch
from src.controllers.customer_controller import CustomerController

class TestCustomerController(unittest.TestCase):
    def setUp(self):
        self.customer_controller = CustomerController()

    @patch('src.controllers.customer_controller.get_db')
    def test_add_customer(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        customer = self.customer_controller.add_customer("John", "Doe", "123 Mano gatve", 1, "89898989")
        self.assertIsNotNone(customer)
        mock_db.add.assert_called()
        mock_db.commit.assert_called()

    @patch('src.controllers.customer_controller.get_db')
    def test_edit_customer(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(id=1)
        customer = self.customer_controller.edit_customer(1,"Johnny", "Baby", "Killa100@yomom.glhf",+3706969420, address="456 Elm St")
        self.assertIsNotNone(customer)
        mock_db.commit.assert_called()

    @patch('src.controllers.customer_controller.get_db')
    def test_delete_customer(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(id=1)
        self.customer_controller.delete_customer(1)
        mock_db.delete.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()