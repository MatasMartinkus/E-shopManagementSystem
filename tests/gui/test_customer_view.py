import unittest
from unittest.mock import MagicMock
import tkinter as tk
from src.gui.customer_view import CustomerView
from ttkbootstrap import Style

class TestCustomerView(unittest.TestCase):
    def setUp(self):
        self.master = tk.Tk()
        self.user = MagicMock()
        self.product_controller = MagicMock()
        self.order_controller = MagicMock()
        self.customer_controller = MagicMock()
        self.customer_view = CustomerView(self.master, self.user, self.product_controller, self.order_controller, self.customer_controller)

    def tearDown(self):
        self.master.destroy()

    def test_load_products(self):
        self.product_controller.get_all_products.return_value = [
            MagicMock(id=1, name="Product1", description="Description1", price=10.0, stock_quantity=10),
            MagicMock(id=2, name="Product2", description="Description2", price=20.0, stock_quantity=20)
        ]
        self.customer_view.load_products()
        self.assertEqual(len(self.customer_view.tree.get_children()), 2)

    def test_add_to_cart(self):
        self.customer_view.selected_product_id = 1
        self.customer_view.quantity_entry.insert(0, "5")
        self.customer_view.add_to_cart()
        self.assertEqual(len(self.customer_view.cart), 1)

    def test_checkout(self):
        self.customer_view.cart = [(MagicMock(id=1, name="Product1", price=10.0), 5)]
        self.customer_controller.get_customer_by_user_id.return_value = MagicMock(id=1)
        self.order_controller.add_order.return_value = MagicMock(id=1)
        self.customer_view.checkout()
        self.order_controller.add_order.assert_called()

    def test_search_products(self):
        self.customer_view.search_entry.insert(0, "Product1")
        self.customer_view.filter_var.set("Name")
        self.product_controller.search_products.return_value = [
            MagicMock(id=1, name="Product1", description="Description1", price=10.0, stock_quantity=10)
        ]
        self.customer_view.search_products()
        self.assertEqual(len(self.customer_view.tree.get_children()), 1)

if __name__ == '__main__':
    unittest.main()