import tkinter as tk
from tkinter import messagebox, ttk

class OrderView:
    def __init__(self, master, order_controller):
        self.master = master
        self.order_controller = order_controller
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame, text="Order Management")
        self.label.pack()

        self.search_label = tk.Label(self.frame, text="Search")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.pack()

        self.filter_label = tk.Label(self.frame, text="Filter by")
        self.filter_label.pack()
        self.filter_var = tk.StringVar()
        self.filter_combobox = ttk.Combobox(self.frame, textvariable=self.filter_var)
        self.filter_combobox['values'] = ("Date Created", "Customer ID", "Product ID")
        self.filter_combobox.pack()

        self.search_button = tk.Button(self.frame, text="Search", command=self.search_orders)
        self.search_button.pack()

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Customer ID", "Date Created", "Product ID"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Customer ID", text="Customer ID")
        self.tree.heading("Date Created", text="Date Created")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_tree_select)

        self.customer_id_label = tk.Label(self.frame, text="Customer ID")
        self.customer_id_label.pack()
        self.customer_id_entry = tk.Entry(self.frame)
        self.customer_id_entry.pack()

        self.product_id_label = tk.Label(self.frame, text="Product ID")
        self.product_id_label.pack()
        self.product_id_entry = tk.Entry(self.frame)
        self.product_id_entry.pack()

        self.delete_button = tk.Button(self.frame, text="Delete Order", command=self.delete_order)
        self.delete_button.pack()

        self.load_orders()

    def load_orders(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        orders = self.order_controller.get_all_orders()
        for order in orders:
            products = ", ".join([f"{product.product_id} (x{product.quantity})" for product in order.products])
            self.tree.insert("", "end", values=(order.id, order.customer_id, order.date_created, products))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        order_id, customer_id, date_created, product_id = self.tree.item(selected_item, "values")
        self.customer_id_entry.delete(0, tk.END)
        self.customer_id_entry.insert(0, customer_id)
        self.product_id_entry.delete(0, tk.END)
        self.product_id_entry.insert(0, product_id)
        self.selected_order_id = order_id
        self.selected_product_id = product_id
        self.show_order_details(order_id)


    def delete_order(self):
        if hasattr(self, 'selected_order_id'):
            order_id = self.selected_order_id
            self.order_controller.delete_order(order_id)
            messagebox.showinfo("Success", "Order deleted successfully")
            self.load_orders()
        else:
            messagebox.showwarning("Warning", "No order selected")

    def show_order_details(self, order_id):
        order = self.order_controller.get_order_by_id(order_id)
        if not order:
            return

        details_window = tk.Toplevel(self.master)
        details_window.title(f"Order Details - Order ID: {order.id}")

        label = tk.Label(details_window, text=f"Order ID: {order.id}\nCustomer ID: {order.customer_id}\nDate Created: {order.date_created}")
        label.pack(pady=10)

        products_tree = ttk.Treeview(details_window, columns=("Product ID", "Quantity", "Name", "Price"), show='headings')
        products_tree.heading("Product ID", text="Product ID")
        products_tree.heading("Quantity", text="Quantity")
        products_tree.heading("Name", text="Name")
        products_tree.heading("Price", text="Price")
        products_tree.pack(fill=tk.BOTH, expand=True)

        for product in order.products:
            products_tree.insert("", "end", values=(product.product_id, product.quantity, product.name, product.price),)

        close_button = ttk.Button(details_window, text="Close", command=details_window.destroy)
        close_button.pack(pady=10)
    
    def search_orders(self):
        search_term = self.search_entry.get()
        filter_by = self.filter_var.get()
        for row in self.tree.get_children():
            self.tree.delete(row)
        orders = self.order_controller.search_orders(search_term, filter_by)
        for order in orders:
            products = ", ".join([f"{product.product_id} (x{product.quantity})" for product in order.products])
            self.tree.insert("", "end", values=(order.id, order.customer_id, order.date_created, products))
