import tkinter as tk
from tkinter import messagebox, ttk

class FinancialView:
    def __init__(self, master, financial_controller):
        self.master = master
        self.financial_controller = financial_controller
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame, text="Financial Management")
        self.label.pack()

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Date", "Amount", "Type", "Recipient", "Sender"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Recipient", text="Recipient")
        self.tree.heading("Sender", text="Sender")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_tree_select)

        self.date_label = tk.Label(self.frame, text="Transaction Date")
        self.date_label.pack()
        self.date_entry = tk.Entry(self.frame)
        self.date_entry.pack()

        self.amount_label = tk.Label(self.frame, text="Amount")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.frame)
        self.amount_entry.pack()

        self.type_label = tk.Label(self.frame, text="Transaction Type")
        self.type_label.pack()
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(self.frame, textvariable=self.type_var)
        self.type_dropdown['values'] = self.financial_controller.TRANSACTION_TYPES
        self.type_dropdown.pack()

        self.recipient_label = tk.Label(self.frame, text="Recipient")
        self.recipient_label.pack()
        self.recipient_entry = tk.Entry(self.frame)
        self.recipient_entry.pack()

        self.sender_label = tk.Label(self.frame, text="Sender")
        self.sender_label.pack()
        self.sender_entry = tk.Entry(self.frame)
        self.sender_entry.pack()

        self.add_button = tk.Button(self.frame, text="Add Transaction", command=self.add_transaction)
        self.add_button.pack()

        self.update_button = tk.Button(self.frame, text="Update Transaction", command=self.update_transaction)
        self.update_button.pack()

        self.delete_button = tk.Button(self.frame, text="Delete Transaction", command=self.delete_transaction)
        self.delete_button.pack()

        self.load_transactions()

    def load_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        transactions = self.financial_controller.get_all_transactions()
        for transaction in transactions:
            self.tree.insert("", "end", values=(transaction.id, transaction.transaction_date, transaction.amount, transaction.transaction_type, transaction.recipient, transaction.sender))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        transaction_id, transaction_date, amount, transaction_type, recipient, sender = self.tree.item(selected_item, "values")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, transaction_date)
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, amount)
        self.type_var.set(transaction_type)
        self.recipient_entry.delete(0, tk.END)
        self.recipient_entry.insert(0, recipient)
        self.sender_entry.delete(0, tk.END)
        self.sender_entry.insert(0, sender)
        self.selected_transaction_id = transaction_id

    def add_transaction(self):
        transaction_date = self.date_entry.get()
        amount = float(self.amount_entry.get())
        transaction_type = self.type_var.get()
        recipient = self.recipient_entry.get()
        sender = self.sender_entry.get()
        self.financial_controller.add_transaction(transaction_date, amount, transaction_type, recipient, sender)
        messagebox.showinfo("Success", "Transaction added successfully")
        self.load_transactions()

    def update_transaction(self):
        if hasattr(self, 'selected_transaction_id'):
            transaction_id = self.selected_transaction_id
            transaction_date = self.date_entry.get()
            amount = float(self.amount_entry.get())
            transaction_type = self.type_var.get()
            recipient = self.recipient_entry.get()
            sender = self.sender_entry.get()
            self.financial_controller.edit_transaction(transaction_id, transaction_date, amount, transaction_type, recipient, sender)
            messagebox.showinfo("Success", "Transaction updated successfully")
            self.load_transactions()
        else:
            messagebox.showwarning("Warning", "No transaction selected")

    def delete_transaction(self):
        if hasattr(self, 'selected_transaction_id'):
            transaction_id = self.selected_transaction_id
            self.financial_controller.delete_transaction(transaction_id)
            messagebox.showinfo("Success", "Transaction deleted successfully")
            self.load_transactions()
        else:
            messagebox.showwarning("Warning", "No transaction selected")