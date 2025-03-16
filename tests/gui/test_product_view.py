import unittest
from unittest.mock import MagicMock
import tkinter as tk
from src.gui.product_view import ProductView

class TestProductView(unittest.TestCase):

    def setUp(self):
        self.master = tk.Tk()
        self.product_controller = MagicMock()
        self.warehouse_controller = MagicMock()
        self.product_view = ProductView(self.master, self.product_controller, self.warehouse_controller)

    def tearDown(self):
        self.master.destroy()


if __name__ == '__main__':
    unittest.main()