import unittest
from unittest.mock import MagicMock
import tkinter as tk
from src.gui.financial_view import FinancialView


class TestFinancialView(unittest.TestCase):
    def setUp(self):
        self.master = tk.Tk()
        self.financial_controller = MagicMock()
        self.financial_view = FinancialView(self.master, self.financial_controller)

    def tearDown(self):
        self.master.destroy()

    def test_load_transactions(self):
        self.financial_controller.get_all_transactions.return_value = [
            MagicMock(id=1, transaction_date="2023-01-01", amount=100.0, transaction_type="Income", recipient="Recipient1", sender="Sender1"),
            MagicMock(id=2, transaction_date="2023-01-02", amount=200.0, transaction_type="Expense", recipient="Recipient2", sender="Sender2")
        ]
        self.financial_view.load_transactions()
        self.assertEqual(len(self.financial_view.tree.get_children()), 2)

    def test_add_transaction(self):
        self.financial_view.date_entry.insert(0, "2023-01-01")
        self.financial_view.amount_entry.insert(0, "100.0")
        self.financial_view.type_var.set("Income")
        self.financial_view.recipient_entry.insert(0, "Recipient1")
        self.financial_view.sender_entry.insert(0, "Sender1")
        self.financial_view.add_transaction()
        self.financial_controller.add_transaction.assert_called()

    def test_update_transaction(self):
        self.financial_view.selected_transaction_id = 1
        self.financial_view.date_entry.insert(0, "2023-01-01")
        self.financial_view.amount_entry.insert(0, "150.0")
        self.financial_view.type_var.set("Income")
        self.financial_view.recipient_entry.insert(0, "Recipient1 Updated")
        self.financial_view.sender_entry.insert(0, "Sender1 Updated")
        self.financial_view.update_transaction()
        self.financial_controller.edit_transaction.assert_called()

    def test_delete_transaction(self):
        self.financial_view.selected_transaction_id = 1
        self.financial_view.delete_transaction()
        self.financial_controller.delete_transaction.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()