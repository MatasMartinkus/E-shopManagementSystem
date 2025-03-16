import unittest
from unittest.mock import MagicMock, patch
from src.controllers.admin_controller import AdminController

class TestAdminController(unittest.TestCase):
    def setUp(self):
        self.admin_controller = AdminController()

    @patch('src.controllers.admin_controller.get_db')
    def test_add_admin(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        admin = self.admin_controller.add_admin("IT", "III", 1)
        self.assertIsNotNone(admin)
        mock_db.add.assert_called()
        mock_db.commit.assert_called()

if __name__ == '__main__':
    unittest.main()