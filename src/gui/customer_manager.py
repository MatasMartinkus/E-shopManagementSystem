import tkinter as tk
from tkinter import messagebox, ttk
from src.models.customer import Customer
from sqlalchemy.orm import joinedload
from src.utils.dbengine import get_db

class CustomerManager:
    def __init__(self, master, customer_controller, order_controller):
        self.master = master
        self.customer_controller = customer_controller
        self.order_controller = order_controller
        self.selected_customer_id = None

        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame, text="Customer Management")
        self.label.pack()

        self.search_label = tk.Label(self.frame, text="Search")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.pack()

        self.filter_label = tk.Label(self.frame, text="Filter by")
        self.filter_label.pack()
        self.filter_var = tk.StringVar()
        self.filter_combobox = ttk.Combobox(self.frame, textvariable=self.filter_var)
        self.filter_combobox['values'] = ("Name", "Email", "Address")
        self.filter_combobox.pack()

        self.search_button = tk.Button(self.frame, text="Search", command=self.search_customers)
        self.search_button.pack()

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Name", "Last Name", "Email", "Phone", "Address"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Address", text="Address")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_tree_select)

        self.name_label = tk.Label(self.frame, text="Name")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack()

        self.last_name_label = tk.Label(self.frame, text="Last Name")
        self.last_name_label.pack()
        self.last_name_entry = tk.Entry(self.frame)
        self.last_name_entry.pack()

        self.email_label = tk.Label(self.frame, text="Email")
        self.email_label.pack()
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack()

        self.phone_label = tk.Label(self.frame, text="Phone")
        self.phone_label.pack()
        self.phone_entry = tk.Entry(self.frame)
        self.phone_entry.pack()

        self.address_label = tk.Label(self.frame, text="Address")
        self.address_label.pack()
        self.address_entry = tk.Entry(self.frame)
        self.address_entry.pack()

        self.update_button = tk.Button(self.frame, text="Update Customer", command=self.update_customer)
        self.update_button.pack()

        self.delete_button = tk.Button(self.frame, text="Delete Customer", command=self.delete_customer)
        self.delete_button.pack()

        self.load_customers()

    def load_customers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        customers = self.customer_controller.get_all_customers()
        for customer in customers:
            self.tree.insert("", "end", values=(customer.id, customer.name, customer.last_name, customer.email, customer.phone, customer.address))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        customer_id, name, last_name, email, phone, address = self.tree.item(selected_item, "values")
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)
        self.last_name_entry.delete(0, tk.END)
        self.last_name_entry.insert(0, last_name)
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, email)
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, phone)
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, address)
        self.selected_customer_id = customer_id

    def update_customer(self):
        if self.selected_customer_id:
            customer_id = self.selected_customer_id
            name = self.name_entry.get()
            last_name = self.last_name_entry.get()
            email = self.email_entry.get()
            phone = self.phone_entry.get()
            address = self.address_entry.get()
            self.customer_controller.edit_customer(customer_id, name, last_name, email, phone, address)
            messagebox.showinfo("Success", "Customer updated successfully")
            self.load_customers()
        else:
            messagebox.showwarning("Warning", "No customer selected")

    def delete_customer(self):
        if self.selected_customer_id:
            customer_id = self.selected_customer_id
            self.customer_controller.delete_customer(customer_id)
            messagebox.showinfo("Success", "Customer deleted successfully")
            self.load_customers()
        else:
            messagebox.showwarning("Warning", "No customer selected")

    def get_customer_by_user_id(self, user_id):
        with get_db() as db:
            return db.query(Customer).options(joinedload(Customer.user)).filter(Customer.user_id == user_id).first()
    
    def search_customers(self):
        search_term = self.search_entry.get()
        filter_by = self.filter_var.get()
        for row in self.tree.get_children():
            self.tree.delete(row)
        customers = self.customer_controller.search_customers(search_term, filter_by)
        for customer in customers:
            self.tree.insert("", "end", values=(customer.id, customer.name, customer.last_name, customer.email, customer.phone, customer.address))
