import unittest
from unittest.mock import MagicMock, patch
from src.controllers.auth_controller import AuthController

class TestAuthController(unittest.TestCase):
    def setUp(self):
        self.email_controller = MagicMock()
        self.customer_controller = MagicMock()
        self.admin_controller = MagicMock()
        self.manager_controller = MagicMock()
        self.auth_controller = AuthController(
            self.email_controller,
            self.customer_controller,
            self.admin_controller,
            self.manager_controller
        )

    @patch('src.controllers.auth_controller.get_db')
    def test_register_user(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        user = self.auth_controller.register_user("testuser", "test@example.com", "password123", "customer")
        self.assertIsNotNone(user)
        mock_db.add.assert_called()
        mock_db.commit.assert_called()

    @patch('src.controllers.auth_controller.get_db')
    def test_authenticate_user(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(username="testuser", hashed_password=self.auth_controller.get_password_hash("password123"))
        user = self.auth_controller.authenticate_user("testuser", "password123")
        self.assertIsNotNone(user)

    def test_get_password_hash(self):
        hashed_password = self.auth_controller.get_password_hash("password123")
        self.assertTrue(self.auth_controller.verify_password("password123", hashed_password))

    def test_verify_password(self):
        hashed_password = self.auth_controller.get_password_hash("password123")
        self.assertTrue(self.auth_controller.verify_password("password123", hashed_password))

if __name__ == '__main__':
    unittest.main()