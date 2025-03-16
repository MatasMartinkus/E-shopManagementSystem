import unittest
from unittest.mock import MagicMock
import tkinter as tk

from src.gui.main_window import MainWindow

class TestMainWindow(unittest.TestCase):

    def setUp(self):
        self.auth_controller = MagicMock()
        self.product_controller = MagicMock()
        self.order_controller = MagicMock()
        self.warehouse_controller = MagicMock()
        self.financial_controller = MagicMock()
        self.admin_controller = MagicMock()
        self.manager_controller = MagicMock()
        self.customer_controller = MagicMock()
        self.email_controller = MagicMock()
        self.main_window = MainWindow(
            self.auth_controller,
            self.product_controller,
            self.order_controller,
            self.warehouse_controller,
            self.financial_controller,
            self.admin_controller,
            self.manager_controller,
            self.customer_controller,
            self.email_controller
        )

    def tearDown(self):
        self.main_window.root.destroy()



if __name__ == '__main__':
    unittest.main()