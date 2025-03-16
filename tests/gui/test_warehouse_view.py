import unittest
from unittest.mock import MagicMock
import tkinter as tk
from src.gui.warehouse_view import WarehouseView
from ttkbootstrap import Style


class TestWarehouseView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.style = Style(theme='cosmo')
    def setUp(self):
        self.master = tk.Tk()
        self.warehouse_controller = MagicMock()
        self.warehouse_view = WarehouseView(self.master, self.warehouse_controller)

    def tearDown(self):
        self.master.destroy()


if __name__ == '__main__':
    unittest.main()