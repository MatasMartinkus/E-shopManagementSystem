import tkinter as tk
from tkinter import messagebox, ttk

class CustomerView:
    def __init__(self, master, user, product_controller, order_controller, customer_controller):
        self.master = master
        self.user = user
        self.product_controller = product_controller
        self.order_controller = order_controller
        self.customer_controller = customer_controller
        self.cart = []

        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame, text="Product Selection")
        self.label.pack()

        self.search_label = tk.Label(self.frame, text="Search")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.pack()

        self.filter_label = tk.Label(self.frame, text="Filter by")
        self.filter_label.pack()
        self.filter_var = tk.StringVar()
        self.filter_combobox = ttk.Combobox(self.frame, textvariable=self.filter_var)
        self.filter_combobox['values'] = ("Name", "Description", "Category", "Subcategory")
        self.filter_combobox.pack()

        self.search_button = tk.Button(self.frame, text="Search", command=self.search_products)
        self.search_button.pack()

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Name", "Description", "Price", "Stock", "Warehouse"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Warehouse", text="Warehouse")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_tree_select)


        self.quantity_label = tk.Label(self.frame, text="Quantity")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(self.frame)
        self.quantity_entry.pack()

        self.add_to_cart_button = tk.Button(self.frame, text="Add to Cart", command=self.add_to_cart)
        self.add_to_cart_button.pack()

        self.view_cart_button = tk.Button(self.frame, text="View Cart", command=self.view_cart)
        self.view_cart_button.pack()

        self.checkout_button = tk.Button(self.frame, text="Checkout", command=self.checkout)
        self.checkout_button.pack()

        self.load_products()

    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        products = self.product_controller.get_all_products()
        for product in products:
            warehouse = self.product_controller.get_warehouse_for_product(product.id)
            warehouse_location = warehouse.location if warehouse else "Unknown"
            self.tree.insert("", "end", values=(product.id, product.name, product.description, product.price, product.stock_quantity, warehouse_location))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        product_id, name, description, price, stock, warehouse = self.tree.item(selected_item, "values")
        self.selected_product_id = product_id
        self.selected_product_name = name
        self.selected_product_price = price
        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, 0)


    def add_to_cart(self):
        if hasattr(self, 'selected_product_id'):
            product_id = self.selected_product_id
            quantity = int(self.quantity_entry.get())
            product = self.product_controller.get_product_by_id(product_id)
            self.cart.append((product, quantity))
            messagebox.showinfo("Success", "Product added to cart")
        else:
            messagebox.showwarning("Warning", "No product selected")

    def view_cart(self):
        cart_window = tk.Toplevel(self.master)
        cart_window.title("Cart")

        cart_tree = ttk.Treeview(cart_window, columns=("Product ID", "Name", "Price", "Quantity"), show='headings')
        cart_tree.heading("Product ID", text="Product ID")
        cart_tree.heading("Name", text="Name")
        cart_tree.heading("Price", text="Price")
        cart_tree.heading("Quantity", text="Quantity")
        cart_tree.pack(fill=tk.BOTH, expand=True)

        for product, quantity in self.cart:
            cart_tree.insert("", "end", values=(product.id, product.name, product.price, quantity))

        def remove_from_cart():
            selected_item = cart_tree.selection()[0]
            for item in cart_tree.get_children():
                if item == selected_item:
                    cart_item_number = cart_tree.index(item)
            self.cart.remove(self.cart[cart_item_number])
            cart_tree.delete(selected_item)
        
        remove_button = ttk.Button(cart_window, text="Remove Selected", command=remove_from_cart)
        remove_button.pack(pady=10)

        close_button = ttk.Button(cart_window, text="Close", command=cart_window.destroy)
        close_button.pack(pady=10)

    def checkout(self):
        if self.cart:
            customer = self.customer_controller.get_customer_by_user_id(self.user.id)
            if not customer:
                messagebox.showerror("Error", "Customer not found")
                return
            customer_id = customer.id
            order = self.order_controller.add_order(customer_id, self.cart)
            if order:
                messagebox.showinfo("Success", "Order placed successfully")
                self.cart.clear()
            else:
                messagebox.showerror("Error", "Failed to place order")
        else:
            messagebox.showwarning("Warning", "Cart is empty")

    def search_products(self):
        search_term = self.search_entry.get()
        filter_by = self.filter_var.get()
        for row in self.tree.get_children():
            self.tree.delete(row)
        products = self.product_controller.search_products(search_term, filter_by)
        for product in products:
            warehouse = self.product_controller.get_warehouse_for_product(product.id)
            warehouse_location = warehouse.location if warehouse else "Unknown"
            self.tree.insert("", "end", values=(product.id, product.name, product.description, product.price, product.stock_quantity, warehouse_location))