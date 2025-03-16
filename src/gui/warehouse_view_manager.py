import tkinter as tk
from tkinter import messagebox, ttk
import datetime

class WarehouseManagerView:
    def __init__(self, master, warehouse_controller, manager_controller, user_id, product_controller, financial_controller, email_controller):
        self.master = master
        self.warehouse_controller = warehouse_controller
        self.manager_controller = manager_controller
        self.product_controller = product_controller
        self.financial_controller = financial_controller
        self.email_controller = email_controller

        self.locations = self.warehouse_controller.get_all_locations()
        self.user_id = user_id
        self.manager = self.manager_controller.get_manager_by_user_id(self.user_id)

        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.show_warehouse_tab()
        self.create_add_admin_tab()
        self.warehouse_items_tab()

    def show_warehouse_tab(self):
        self.warehouse_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.warehouse_tab, text="Manage Warehouses")

        self.label = tk.Label(self.warehouse_tab, text="Warehouse Management")
        self.label.pack()

        self.tree = ttk.Treeview(self.warehouse_tab, columns=("ID", "Location", "Capacity", "Max Volume", "Max Weight", "Current Volume", "Current Weight"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Capacity", text="Capacity")
        self.tree.heading("Max Volume", text="Max Volume")
        self.tree.heading("Max Weight", text="Max Weight")
        self.tree.heading("Current Volume", text="Current Volume")
        self.tree.heading("Current Weight", text="Current Weight")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_warehouse_tree_select)

        self.location_label = tk.Label(self.warehouse_tab, text="Location")
        self.location_label.pack()
        self.location_var = tk.StringVar()
        self.location_combobox = ttk.Combobox(self.warehouse_tab, textvariable=self.location_var)
        self.location_combobox['values'] = self.locations
        self.location_combobox.pack()

        self.capacity_label = tk.Label(self.warehouse_tab, text="Capacity")
        self.capacity_label.pack()
        self.capacity_entry = tk.Entry(self.warehouse_tab)
        self.capacity_entry.pack()

        self.max_volume_label = tk.Label(self.warehouse_tab, text="Max Volume")
        self.max_volume_label.pack()
        self.max_volume_entry = tk.Entry(self.warehouse_tab)
        self.max_volume_entry.pack()

        self.max_weight_label = tk.Label(self.warehouse_tab, text="Max Weight")
        self.max_weight_label.pack()
        self.max_weight_entry = tk.Entry(self.warehouse_tab)
        self.max_weight_entry.pack()

        self.current_volume_label = tk.Label(self.warehouse_tab, text="Current Volume")
        self.current_volume_label.pack()
        self.current_volume_entry = tk.Entry(self.warehouse_tab)
        self.current_volume_entry.pack()

        self.current_weight_label = tk.Label(self.warehouse_tab, text="Current Weight")
        self.current_weight_label.pack()
        self.current_weight_entry = tk.Entry(self.warehouse_tab)
        self.current_weight_entry.pack()

        self.update_button = tk.Button(self.warehouse_tab, text="Update Warehouse", command=self.update_warehouse)
        self.update_button.pack()

        self.delete_button = tk.Button(self.warehouse_tab, text="Delete Warehouse", command=self.delete_warehouse)
        self.delete_button.pack()

        self.load_warehouses()


    def create_add_admin_tab(self):
        self.add_admin_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_admin_frame, text="Manage Warehouse Administrators")

        self.admin_tree = ttk.Treeview(self.add_admin_frame, columns=("ID", "Name", "Last Name", "DOB", "Hourly Rate", "Start Date","End Date", "Job Title"), show='headings')
        self.admin_tree.heading("ID", text="ID")
        self.admin_tree.heading("Name", text="Name")
        self.admin_tree.heading("Last Name", text="Last Name")
        self.admin_tree.heading("DOB", text="DOB")
        self.admin_tree.heading("Hourly Rate", text="Hourly Rate")
        self.admin_tree.heading("Start Date", text="Start Date")
        self.admin_tree.heading("End Date", text="End Date")
        self.admin_tree.heading("Job Title", text="Job Title")
        self.admin_tree.pack(fill=tk.BOTH, expand=True)
        self.admin_tree.bind("<Double-1>", self.on_admin_tree_select)

        self.label = tk.Label(self.add_admin_frame, text="Add Warehouse Administrator")
        self.label.pack()

        self.active_warehouses = self.warehouse_controller.get_all_warehouses()
        self.warehouse_label = tk.Label(self.add_admin_frame, text="Warehouse")
        self.warehouse_label.pack()
        self.warehouse_var = tk.StringVar()
        self.warehouse_combobox = ttk.Combobox(self.add_admin_frame, textvariable=self.warehouse_var)
        self.warehouse_combobox['values'] = [warehouse.location for warehouse in self.active_warehouses]
        self.warehouse_combobox.pack()

        self.name_label = tk.Label(self.add_admin_frame, text="Name")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.add_admin_frame)
        self.name_entry.pack()

        self.last_name_label = tk.Label(self.add_admin_frame, text="Last Name")
        self.last_name_label.pack()
        self.last_name_entry = tk.Entry(self.add_admin_frame)
        self.last_name_entry.pack()

        self.dob_label = tk.Label(self.add_admin_frame, text="Date of Birth (YYYY-MM-DD)")
        self.dob_label.pack()
        self.dob_entry = tk.Entry(self.add_admin_frame)
        self.dob_entry.pack()

        self.hourly_rate_label = tk.Label(self.add_admin_frame, text="Hourly Rate")
        self.hourly_rate_label.pack()
        self.hourly_rate_entry = tk.Entry(self.add_admin_frame)
        self.hourly_rate_entry.pack()

        self.start_date_label = tk.Label(self.add_admin_frame, text="Start Date (YYYY-MM-DD)")
        self.start_date_label.pack()
        self.start_date_entry = tk.Entry(self.add_admin_frame)
        self.start_date_entry.pack()

        self.end_date_label = tk.Label(self.add_admin_frame, text="End Date (YYYY-MM-DD)")
        self.end_date_label.pack()
        self.end_date_entry = tk.Entry(self.add_admin_frame)
        self.end_date_entry.pack()

        self.job_title_label = tk.Label(self.add_admin_frame, text="Job Title")
        self.job_title_label.pack()
        self.job_title_entry = tk.Entry(self.add_admin_frame)
        self.job_title_entry.pack()

        self.add_admin_button = tk.Button(self.add_admin_frame, text="Add Administrator", command=self.add_admin)
        self.add_admin_button.pack()

        self.load_admins()


    def warehouse_items_tab(self):
        self.warehouse_items_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.warehouse_items_tab, text="Manage Warehouse Items")

        self.warehouse_item_tree = ttk.Treeview(self.warehouse_items_tab, columns=("ID", "Name", "Warehouse", "Stock", "Weight", "Length", "Width", "Height"), show='headings')
        self.warehouse_item_tree.heading("ID", text="ID")
        self.warehouse_item_tree.heading("Name", text="Name")  
        self.warehouse_item_tree.heading("Warehouse", text="Warehouse")
        self.warehouse_item_tree.heading("Stock", text="Stock")
        self.warehouse_item_tree.heading("Weight", text="Weight")
        self.warehouse_item_tree.heading("Length", text="Length")
        self.warehouse_item_tree.heading("Width", text="Width")
        self.warehouse_item_tree.heading("Height", text="Height")
        self.warehouse_item_tree.pack(fill=tk.BOTH, expand=True)
        self.warehouse_item_tree.bind("<Double-1>", self.on_warehouse_item_tree_select)

        self.load_warehouse_products()


    def load_warehouse_products(self):
        # Delete all rows in the tree
        for row in self.warehouse_item_tree.get_children():
            self.warehouse_item_tree.delete(row)
            # Get the location of the manager
        manager_location = self.manager.location
        # Get the warehouse ids for the manager's location
        warehouse_ids_for_location = [warehouse.id for warehouse in self.active_warehouses if warehouse.location == manager_location]
        # Get all products for each warehouse
        for warehouse_id in warehouse_ids_for_location:
            products = self.product_controller.get_warehouse_products_by_warehouse_id(warehouse_id)
            for product in products:
                self.warehouse_item_tree.insert("", "end", values=(product.id, product.name, product.warehouse_id, product.stock_quantity, product.weight, product.length, product.width, product.height))



    def load_warehouses(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        manager_location = self.manager.location
        warehouses = self.warehouse_controller.get_all_warehouses()
        for warehouse in warehouses:
            if warehouse.location == manager_location:
                self.tree.insert("", "end", values=(warehouse.id, warehouse.location, warehouse.capacity, warehouse.max_volume, warehouse.max_weight, warehouse.current_volume, warehouse.current_weight))

    def load_admins(self):
        for row in self.admin_tree.get_children():
            self.admin_tree.delete(row)
        manager_location = self.manager.location
        warehouse_ids_for_location = [warehouse.id for warehouse in self.active_warehouses if warehouse.location == manager_location]
        admins = self.warehouse_controller.get_all_administrators()
        for admin in admins:
            if admin.warehouse_id in warehouse_ids_for_location:
                self.admin_tree.insert("", "end", values=(admin.id, admin.name, admin.last_name, admin.dob, admin.hourly_rate, admin.start_date, admin.end_date, admin.job_title))
        

    def on_warehouse_tree_select(self, event):
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
        self.current_volume_entry.insert(0, 0)
        self.current_weight_entry.delete(0, tk.END)
        self.current_weight_entry.insert(0, 0)
        self.selected_warehouse_id = warehouse_id

    def on_admin_tree_select(self, event):
        selected_item = self.admin_tree.selection()[0]
        admin_id, name, last_name, dob, hourly_rate, start_date, end_date, job_title = self.admin_tree.item(selected_item, "values")
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)
        self.last_name_entry.delete(0, tk.END)
        self.last_name_entry.insert(0, last_name)
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, dob)
        self.end_date_entry.delete(0, tk.END)
        self.end_date_entry.insert(0, end_date)
        self.hourly_rate_entry.delete(0, tk.END)
        self.hourly_rate_entry.insert(0, hourly_rate)
        self.start_date_entry.delete(0, tk.END)
        self.start_date_entry.insert(0, start_date)
        self.job_title_entry.delete(0, tk.END)
        self.job_title_entry.insert(0, job_title)
        self.selected_admin_id = admin_id
        self.show_admin_details_window(admin_id)

    def on_warehouse_item_tree_select(self, event):
        selected_item = self.admin_tree.selection()[0]
        item_id, name, warehouse, stock, weight, length, width, height = self.admin_tree.item(selected_item, "values")
        messagebox.showinfo("No functionality", "This feature is not implemented yet")
        self.load_warehouse_products()

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
    
    def add_admin(self):
        name = self.name_entry.get()
        last_name = self.last_name_entry.get()
        dob = self.dob_entry.get()
        hourly_rate = float(self.hourly_rate_entry.get())
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        job_title = self.job_title_entry.get()
        warehouse_id = self.active_warehouses[self.warehouse_combobox.current()].id
        self.warehouse_controller.add_administrator(warehouse_id, name, last_name, dob, hourly_rate, start_date, end_date, job_title)
        messagebox.showinfo("Success", "Warehouse administrator added successfully")
        self.load_admins()
    
    def show_admin_details_window(self, admin_id):
        admin = self.warehouse_controller.get_administrator_by_id(admin_id)
        if not admin:
            return

        details_window = tk.Toplevel(self.master)
        details_window.title(f"Administrator Details - ID: {admin_id}")

        admin_tree = ttk.Treeview(details_window, columns=("Name", "Last name", "Start date", "Job Title", "Hourly Rate",), show='headings')
        admin_tree.heading("Name", text="Name")
        admin_tree.heading("Last name", text="Last name")
        admin_tree.heading("Start date", text="Start date")
        admin_tree.heading("Job Title", text="Job Title")
        admin_tree.heading("Hourly Rate", text="Hourly Rate")
        admin_tree.pack(fill=tk.BOTH, expand=True)

        admin_tree.insert("", "end", values=(admin.name, admin.last_name, admin.start_date, admin.job_title, admin.hourly_rate))

        normal_hours_label = tk.Label(details_window, text="Normal Hours Worked")
        normal_hours_label.pack()
        normal_hours_entry = tk.Entry(details_window)
        normal_hours_entry.pack()

        overtime_hours_label = tk.Label(details_window, text="Overtime Hours Worked")
        overtime_hours_label.pack()
        overtime_hours_entry = tk.Entry(details_window)
        overtime_hours_entry.pack()

        holiday_hours_label = tk.Label(details_window, text="Holiday Hours Worked")
        holiday_hours_label.pack()
        holiday_hours_entry = tk.Entry(details_window)
        holiday_hours_entry.pack()

        calculate_salary_button = tk.Button(details_window, text="Calculate Salary", command=lambda: self.calculate_salary(admin.id, normal_hours_entry.get(), overtime_hours_entry.get(), holiday_hours_entry.get()))
        calculate_salary_button.pack()

        close_button = ttk.Button(details_window, text="Close", command=details_window.destroy)
        close_button.pack(pady=10)

    def calculate_salary(self, admin_id, normal_hours, overtime_hours, holiday_hours):
        admin = self.warehouse_controller.get_administrator_by_id(admin_id)
        normal_hours = float(normal_hours)
        overtime_hours = float(overtime_hours)
        holiday_hours = float(holiday_hours)
        hourly_rate = admin.hourly_rate
        transaction_date=datetime.datetime.utcnow()
        def calculate_coefficient():
            coefficient = 1
            for i in range(10):
                try:
                    exact_date = transaction_date.replace(year=transaction_date.year + i)
                except ValueError:
                    exact_date = transaction_date.replace(month=2, day=28, year=transaction_date.year + i)
                if admin.start_date <= transaction_date:
                    coefficient += 0.1
            return coefficient
        if not admin:
            return
        coefficient = calculate_coefficient()
        salary = (normal_hours + overtime_hours * 1.5 + holiday_hours * 2) * hourly_rate * coefficient
        if salary:
            payslip = self.financial_controller.add_transaction(transaction_date=transaction_date, amount=salary, transaction_type="Transfer", recipient=f"{admin.name} {admin.last_name}", sender="Employer", email_controller=False)
        if payslip:
            messagebox.showinfo("Salary Calculation", f"Salary calculated successfully. Payslip ID: {payslip.id}")
        
        
    