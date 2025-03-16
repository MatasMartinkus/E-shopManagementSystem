import unittest
from unittest.mock import MagicMock, patch
from src.controllers.manager_controller import ManagerController

class TestManagerController(unittest.TestCase):
    def setUp(self):
        self.manager_controller = ManagerController()

    @patch('src.controllers.manager_controller.get_db')
    def test_add_manager(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        manager = self.manager_controller.add_manager("Location1", "III", 1)
        self.assertIsNotNone(manager)
        mock_db.add.assert_called()
        mock_db.commit.assert_called()

    @patch('src.controllers.manager_controller.get_db')
    def test_get_manager_by_user_id(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(id=1, user_id=1)
        manager = self.manager_controller.get_manager_by_user_id(1)
        self.assertIsNotNone(manager)

if __name__ == '__main__':
    unittest.main()