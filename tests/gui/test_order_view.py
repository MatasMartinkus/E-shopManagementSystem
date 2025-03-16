import unittest
from unittest.mock import MagicMock
import tkinter as tk
from src.gui.order_view import OrderView


class TestOrderView(unittest.TestCase):
    def setUp(self):
        self.master = tk.Tk()
        self.order_controller = MagicMock()
        self.order_view = OrderView(self.master, self.order_controller)

    def tearDown(self):
        self.master.destroy()


if __name__ == '__main__':
    unittest.main()