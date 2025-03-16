import unittest
from unittest.mock import MagicMock
import tkinter as tk
from src.gui.customer_dashboard import CustomerDashboard

class TestCustomerDashboard(unittest.TestCase):
    def setUp(self):
        self.master = tk.Tk()
        self.product_controller = MagicMock()
        self.order_controller = MagicMock()
        self.customer_controller = MagicMock()
        self.user = MagicMock()
        self.customer_dashboard = CustomerDashboard(self.master, self.product_controller, self.order_controller, self.customer_controller, self.user)

    def tearDown(self):
        self.master.destroy()

if __name__ == '__main__':
    unittest.main()