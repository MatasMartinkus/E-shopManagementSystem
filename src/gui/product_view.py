import tkinter as tk
from tkinter import messagebox, ttk

class ProductView:
    def __init__(self, master, product_controller, warehouse_controller):
        self.master = master
        self.product_controller = product_controller
        self.warehouse_controller = warehouse_controller
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame, text="Product Management")
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

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Name", "Description", "Price", "Stock", "Category", "Subcategory", "Length", "Width", "Height", "Weight","Warehouse"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Subcategory", text="Subcategory")
        self.tree.heading("Length", text="Length")
        self.tree.heading("Width", text="Width")
        self.tree.heading("Height", text="Height")
        self.tree.heading("Weight", text="Weight")
        self.tree.heading("Warehouse", text="Warehouse")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_tree_select)

        self.name_label = tk.Label(self.frame, text="Name")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack()

        self.description_label = tk.Label(self.frame, text="Description")
        self.description_label.pack()
        self.description_entry = tk.Entry(self.frame)
        self.description_entry.pack()

        self.price_label = tk.Label(self.frame, text="Price")
        self.price_label.pack()
        self.price_entry = tk.Entry(self.frame)
        self.price_entry.pack()

        self.stock_label = tk.Label(self.frame, text="Stock Quantity")
        self.stock_label.pack()
        self.stock_entry = tk.Entry(self.frame)
        self.stock_entry.pack()

        self.category_label = tk.Label(self.frame, text="Category")
        self.category_label.pack()
        self.category_entry = tk.Entry(self.frame)
        self.category_entry.pack()

        self.subcategory_label = tk.Label(self.frame, text="Subcategory")
        self.subcategory_label.pack()
        self.subcategory_entry = tk.Entry(self.frame)
        self.subcategory_entry.pack()

        self.length_label = tk.Label(self.frame, text="Length")
        self.length_label.pack()
        self.length_entry = tk.Entry(self.frame)
        self.length_entry.pack()

        self.width_label = tk.Label(self.frame, text="Width")
        self.width_label.pack()
        self.width_entry = tk.Entry(self.frame)
        self.width_entry.pack()

        self.height_label = tk.Label(self.frame, text="Height")
        self.height_label.pack()
        self.height_entry = tk.Entry(self.frame)
        self.height_entry.pack()

        self.weight_label = tk.Label(self.frame, text="Weight")
        self.weight_label.pack()
        self.weight_entry = tk.Entry(self.frame)
        self.weight_entry.pack()

        self.warehouse_label = tk.Label(self.frame, text="Warehouse")
        self.warehouse_var = tk.StringVar()
        self.warehouse_label.pack()
        self.warehouse_combobox = ttk.Combobox(self.frame, textvariable=self.warehouse_var)
        self.warehouses = self.warehouse_controller.get_all_warehouses()
        self.warehouse_combobox['values'] = [warehouse.location for warehouse in self.warehouses]
        self.warehouse_combobox.pack()

        self.add_button = tk.Button(self.frame, text="Add Product", command=self.add_product)
        self.add_button.pack()

        self.update_button = tk.Button(self.frame, text="Update Product", command=self.update_product)
        self.update_button.pack()

        self.delete_button = tk.Button(self.frame, text="Delete Product", command=self.delete_product)
        self.delete_button.pack()

        self.load_products()

    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        products = self.product_controller.get_all_products()
        for product in products:
            warehouse = self.product_controller.get_warehouse_for_product(product.id)
            warehouse_location = warehouse.location if warehouse else "Unknown"
            self.tree.insert("", "end", values=(product.id, product.name, product.description, product.price, product.stock_quantity, product.category, product.subcategory, product.length, product.width, product.height, product.weight, warehouse_location))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        product_id, name, description, price, stock_quantity, category, subcategory, length, width, height, weight, warehouse_location = self.tree.item(selected_item, "values")
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)
        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, description)
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, price)
        self.stock_entry.delete(0, tk.END)
        self.stock_entry.insert(0, stock_quantity)
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, category)
        self.subcategory_entry.delete(0, tk.END)
        self.subcategory_entry.insert(0, subcategory)
        self.length_entry.delete(0, tk.END)
        self.length_entry.insert(0, length)
        self.width_entry.delete(0, tk.END)
        self.width_entry.insert(0, width)
        self.height_entry.delete(0, tk.END)
        self.height_entry.insert(0, height)
        self.weight_entry.delete(0, tk.END)
        self.weight_entry.insert(0, weight)
        self.warehouse_combobox.delete(0, tk.END)
        self.warehouse_combobox.insert(0, warehouse_location)
        self.selected_product_id = product_id

    def add_product(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        price = float(self.price_entry.get())
        stock_quantity = int(self.stock_entry.get())
        category = self.category_entry.get()
        subcategory = self.subcategory_entry.get()
        length = float(self.length_entry.get())
        width = float(self.width_entry.get())
        height = float(self.height_entry.get())
        weight = float(self.weight_entry.get())
        warehouse_location = self.warehouse_var.get()
        warehouse = next((warehouse for warehouse in self.warehouses if warehouse.location == warehouse_location), None)
        if not warehouse:
            messagebox.showerror("Error", "Invalid warehouse selected")
            return

        if self.product_controller.add_product(name, description, price, stock_quantity, category, subcategory, length, width, height, weight, warehouse.id):
            messagebox.showinfo("Success", "Product added successfully")
            self.load_products()
        else:
            messagebox.showerror("Not enough space.","Please adjust quantity.")

    def update_product(self):
        if hasattr(self, 'selected_product_id'):
            product_id = self.selected_product_id
            name = self.name_entry.get()
            description = self.description_entry.get()
            price = float(self.price_entry.get())
            stock_quantity = int(self.stock_entry.get())
            category = self.category_entry.get()
            subcategory = self.subcategory_entry.get()
            length = float(self.length_entry.get())
            width = float(self.width_entry.get())
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())
            warehouse_location = self.warehouse_var.get()
            warehouse = next((warehouse for warehouse in self.warehouses if warehouse.location == warehouse_location), None)
            if not warehouse:
                messagebox.showerror("Error", "Invalid warehouse selected")
                return
            self.product_controller.edit_product(product_id, name, description, price, stock_quantity, category, subcategory, length, width, height, weight, warehouse.id)
            messagebox.showinfo("Success", "Product updated successfully")
            self.load_products()
        else:
            messagebox.showwarning("Warning", "No product selected")

    def delete_product(self):
        if hasattr(self, 'selected_product_id'):
            product_id = self.selected_product_id
            self.product_controller.delete_product(product_id)
            messagebox.showinfo("Success", "Product deleted successfully")
            self.load_products()
        else:
            messagebox.showwarning("Warning", "No product selected")

    def search_products(self):
        search_term = self.search_entry.get()
        filter_by = self.filter_var.get()
        for row in self.tree.get_children():
            self.tree.delete(row)
        products = self.product_controller.search_products(search_term, filter_by)
        for product in products:
            warehouse = self.product_controller.get_warehouse_for_product(product.id)
            warehouse_location = warehouse.location if warehouse else "Unknown"
            self.tree.insert("", "end", values=(product.id, product.name, product.description, product.price, product.stock_quantity, product.category, product.subcategory, product.length, product.width, product.height, product.weight, warehouse_location))