import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from src.controllers.email_controller import EmailController

class TestEmailController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.email_controller = EmailController(
            self.app,
            smtp_server="smtp.example.com",
            smtp_port=587,
            smtp_user="user@example.com",
            smtp_password="password"
        )

    @patch('src.controllers.email_controller.smtplib.SMTP')
    def test_send_verification_email(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        token = self.email_controller.generate_verification_token("test@example.com")
        self.email_controller.send_verification_email("test@example.com", token)
        mock_server.sendmail.assert_called()

    def test_generate_verification_token(self):
        token = self.email_controller.generate_verification_token("test@example.com")
        self.assertIsNotNone(token)

    def test_confirm_verification_token(self):
        token = self.email_controller.generate_verification_token("test@example.com")
        email = self.email_controller.confirm_verification_token(token)
        self.assertEqual(email, "test@example.com")

if __name__ == '__main__':
    unittest.main()