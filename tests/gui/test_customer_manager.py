import unittest
from unittest.mock import MagicMock
import tkinter as tk
from src.gui.customer_manager import CustomerManager
from ttkbootstrap import Style

class TestCustomerManager(unittest.TestCase):
    def setUp(self):
        self.master = tk.Tk()
        self.customer_controller = MagicMock()
        self.order_controller = MagicMock()
        self.customer_manager = CustomerManager(self.master, self.customer_controller, self.order_controller)

    def tearDown(self):
        self.master.destroy()

    def test_load_customers(self):
        self.customer_controller.get_all_customers.return_value = [
            MagicMock(id=1, name="Customer1", email="customer1@example.com", address="Address1"),
            MagicMock(id=2, name="Customer2", email="customer2@example.com", address="Address2")
        ]
        self.customer_manager.load_customers()
        self.assertEqual(len(self.customer_manager.tree.get_children()), 2)

    def test_update_customer(self):
        self.customer_manager.selected_customer_id = 1
        self.customer_manager.name_entry.insert(0, "Customer1 Updated")
        self.customer_manager.email_entry.insert(0, "customer1_updated@example.com")
        self.customer_manager.address_entry.insert(0, "Address1 Updated")
        self.customer_manager.update_customer()
        self.customer_controller.edit_customer.assert_called()

    def test_delete_customer(self):
        self.customer_manager.selected_customer_id = 1
        self.customer_manager.delete_customer()
        self.customer_controller.delete_customer.assert_called_with(1)

    def test_search_customers(self):
        self.customer_manager.search_entry.insert(0, "Customer1")
        self.customer_manager.filter_var.set("Name")
        self.customer_controller.search_customers.return_value = [
            MagicMock(id=1, name="Customer1", email="customer1@example.com", address="Address1")
        ]
        self.customer_manager.search_customers()
        self.assertEqual(len(self.customer_manager.tree.get_children()), 1)

if __name__ == '__main__':
    unittest.main()