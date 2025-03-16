import tkinter as tk
from tkinter import messagebox, ttk

class WarehouseView:
    def __init__(self, master, warehouse_controller):
        self.master = master
        self.warehouse_controller = warehouse_controller
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.locations = self.warehouse_controller.get_all_locations()

        self.label = tk.Label(self.frame, text="Warehouse Management")
        self.label.pack()

        self.search_label = tk.Label(self.frame, text="Search")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.pack()

        self.filter_label = tk.Label(self.frame, text="Filter by")
        self.filter_label.pack()
        self.filter_var = tk.StringVar()
        self.filter_combobox = ttk.Combobox(self.frame, textvariable=self.filter_var)
        self.filter_combobox['values'] = ("Location", "Capacity", "Max Volume", "Max Weight")
        self.filter_combobox.pack()

        self.search_button = tk.Button(self.frame, text="Search", command=self.search_warehouses)
        self.search_button.pack()

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Location", "Capacity", "Max Volume", "Max Weight", "Current Volume", "Current Weight"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Capacity", text="Capacity")
        self.tree.heading("Max Volume", text="Max Volume")
        self.tree.heading("Max Weight", text="Max Weight")
        self.tree.heading("Current Volume", text="Current Volume")
        self.tree.heading("Current Weight", text="Current Weight")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_tree_select)

        self.location_label = tk.Label(self.frame, text="Location")
        self.location_label.pack()
        self.location_var = tk.StringVar()
        self.location_combobox = ttk.Combobox(self.frame, textvariable=self.location_var)
        self.location_combobox['values'] = self.locations
        self.location_combobox.pack()

        self.capacity_label = tk.Label(self.frame, text="Capacity")
        self.capacity_label.pack()
        self.capacity_entry = tk.Entry(self.frame)
        self.capacity_entry.pack()

        self.max_volume_label = tk.Label(self.frame, text="Max Volume")
        self.max_volume_label.pack()
        self.max_volume_entry = tk.Entry(self.frame)
        self.max_volume_entry.pack()

        self.max_weight_label = tk.Label(self.frame, text="Max Weight")
        self.max_weight_label.pack()
        self.max_weight_entry = tk.Entry(self.frame)
        self.max_weight_entry.pack()

        self.current_volume_label = tk.Label(self.frame, text="Current Volume")
        self.current_volume_label.pack()
        self.current_volume_entry = tk.Entry(self.frame)
        self.current_volume_entry.pack()

        self.current_weight_label = tk.Label(self.frame, text="Current Weight")
        self.current_weight_label.pack()
        self.current_weight_entry = tk.Entry(self.frame)
        self.current_weight_entry.pack()

        self.add_button = tk.Button(self.frame, text="Add Warehouse", command=self.add_warehouse)
        self.add_button.pack()

        self.update_button = tk.Button(self.frame, text="Update Warehouse", command=self.update_warehouse)
        self.update_button.pack()

        self.delete_button = tk.Button(self.frame, text="Delete Warehouse", command=self.delete_warehouse)
        self.delete_button.pack()

        self.load_warehouses()

    def load_warehouses(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        warehouses = self.warehouse_controller.get_all_warehouses()
        for warehouse in warehouses:
            self.tree.insert("", "end", values=(warehouse.id, warehouse.location, warehouse.capacity, warehouse.max_volume, warehouse.max_weight, warehouse.current_volume, warehouse.current_weight))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        warehouse_id, location, capacity, max_volume, max_weight, current_volume, current_weight = self.tree.item(selected_item, "values")
        self.location_combobox.delete(0, tk.END)
        self.location_combobox.insert(0, location)
        self.capacity_entry.delete(0, tk.END)
        self.capacity_entry.insert(0, capacity)
        self.max_volume_entry.delete(0, tk.END)
        self.max_volume_entry.insert(0, max_volume)
        self.max_weight_entry.delete(0, tk.END)
        self.max_weight_entry.insert(0, max_weight)
        self.current_volume_entry.delete(0, tk.END)
        self.current_volume_entry.insert(0, current_volume)
        self.current_weight_entry.delete(0, tk.END)
        self.current_weight_entry.insert(0, current_weight)
        self.selected_warehouse_id = warehouse_id

    def add_warehouse(self):
        location = self.location_var.get()
        capacity = int(self.capacity_entry.get())
        max_volume = float(self.max_volume_entry.get())
        max_weight = float(self.max_weight_entry.get())

        self.warehouse_controller.add_warehouse(location, capacity, max_volume, max_weight, 0, 0)
        messagebox.showinfo("Success", "Warehouse added successfully")
        self.load_warehouses()

    def update_warehouse(self):
        if hasattr(self, 'selected_warehouse_id'):
            warehouse_id = self.selected_warehouse_id
            location = self.location_var.get()
            capacity = int(self.capacity_entry.get())
            max_volume = float(self.max_volume_entry.get())
            max_weight = float(self.max_weight_entry.get())
            current_volume = float(self.current_volume_entry.get())
            current_weight = float(self.current_weight_entry.get())
            self.warehouse_controller.edit_warehouse(warehouse_id, location, capacity, max_volume, max_weight, current_volume, current_weight)
            messagebox.showinfo("Success", "Warehouse updated successfully")
            self.load_warehouses()
        else:
            messagebox.showwarning("Warning", "No warehouse selected")

    def delete_warehouse(self):
        if hasattr(self, 'selected_warehouse_id'):
            warehouse_id = self.selected_warehouse_id
            self.warehouse_controller.delete_warehouse(warehouse_id)
            messagebox.showinfo("Success", "Warehouse deleted successfully")
            self.load_warehouses()
        else:
            messagebox.showwarning("Warning", "No warehouse selected")

    def search_warehouses(self):
        search_term = self.search_entry.get()
        filter_by = self.filter_var.get()
        for row in self.tree.get_children():
            self.tree.delete(row)
        warehouses = self.warehouse_controller.search_warehouses(search_term, filter_by)
        for warehouse in warehouses:
            self.tree.insert("", "end", values=(warehouse.id, warehouse.location, warehouse.capacity, warehouse.max_volume, warehouse.max_weight, warehouse.current_volume, warehouse.current_weight))
        