import unittest
from unittest.mock import MagicMock
import tkinter as tk
from src.gui.warehouse_view_manager import WarehouseManagerView

class TestWarehouseManagerView(unittest.TestCase):

    def setUp(self):
        self.master = tk.Tk()
        self.warehouse_controller = MagicMock()
        self.manager_controller = MagicMock()
        self.product_controller = MagicMock()
        self.financial_controller = MagicMock()
        self.email_controller = MagicMock()
        self.user_id = 1
        self.warehouse_manager_view = WarehouseManagerView(
            self.master, 
            self.warehouse_controller, 
            self.manager_controller, 
            self.user_id, 
            self.product_controller, 
            self.financial_controller, 
            self.email_controller
        )

    def tearDown(self):
        self.master.destroy()


if __name__ == '__main__':
    unittest.main()