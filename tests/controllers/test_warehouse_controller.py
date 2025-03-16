import unittest
from unittest.mock import MagicMock, patch
from src.controllers.warehouse_controller import WarehouseController

class TestWarehouseController(unittest.TestCase):
    def setUp(self):
        self.warehouse_controller = WarehouseController()

    @patch('src.controllers.warehouse_controller.get_db')
    def test_add_warehouse(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        warehouse = self.warehouse_controller.add_warehouse("Location1", 1000, 10000, 10000)
        self.assertIsNotNone(warehouse)
        mock_db.add.assert_called()
        mock_db.commit.assert_called()

    @patch('src.controllers.warehouse_controller.get_db')
    def test_edit_warehouse(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(id=1)
        warehouse = self.warehouse_controller.edit_warehouse(1, location="Location2")
        self.assertIsNotNone(warehouse)
        mock_db.commit.assert_called()

    @patch('src.controllers.warehouse_controller.get_db')
    def test_delete_warehouse(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(id=1)
        self.warehouse_controller.delete_warehouse(1)
        mock_db.delete.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()