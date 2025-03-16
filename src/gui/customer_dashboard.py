import tkinter as tk
from tkinter import ttk
from src.gui.customer_view import CustomerView

class CustomerDashboard:
    def __init__(self, master, product_controller, order_controller, customer_controller, user):
        self.master = master
        self.product_controller = product_controller
        self.order_controller = order_controller
        self.customer_controller = customer_controller
        self.user = user

        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(self.frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.create_product_tab(notebook)

    def create_product_tab(self, notebook):
        product_frame = ttk.Frame(notebook, padding="10")
        notebook.add(product_frame, text="Products")
        CustomerView(product_frame, self.user, self.product_controller, self.order_controller, self.customer_controller)