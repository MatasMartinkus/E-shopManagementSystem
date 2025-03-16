import unittest
from unittest.mock import MagicMock, patch
from src.controllers.order_controller import OrderController

class TestOrderController(unittest.TestCase):
    def setUp(self):
        self.order_controller = OrderController()

    @patch('src.controllers.order_controller.get_db')
    def test_add_order(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        cart = [(MagicMock(id=1, name="Product1", price=10.0), 2)]
        order = self.order_controller.add_order(1, cart)
        self.assertIsNotNone(order)
        mock_db.add.assert_called()
        mock_db.commit.assert_called()

    @patch('src.controllers.order_controller.get_db')
    def test_edit_order(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(id=1, customer_id=1)
        order = self.order_controller.edit_order(1, customer_id=2)
        self.assertIsNotNone(order)
        mock_db.commit.assert_called()

    @patch('src.controllers.order_controller.get_db')
    def test_delete_order(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(id=1)
        self.order_controller.delete_order(1)
        mock_db.delete.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()