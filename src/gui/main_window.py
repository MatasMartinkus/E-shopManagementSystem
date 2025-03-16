import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from validate_email_address import validate_email
from datetime import datetime
from src.gui.product_view import ProductView
from src.gui.order_view import OrderView
from src.gui.customer_view import CustomerView
from src.gui.warehouse_view import WarehouseView
from src.gui.financial_view import FinancialView
from src.gui.customer_dashboard import CustomerDashboard
from src.gui.customer_manager import CustomerManager
from src.gui.warehouse_view_manager import WarehouseManagerView

class MainWindow:
    def __init__(self, auth_controller, product_controller, order_controller, warehouse_controller, financial_controller, admin_controller, manager_controller, customer_controller, email_controller):
        self.email_controller = email_controller
        self.auth_controller = auth_controller
        self.product_controller = product_controller
        self.order_controller = order_controller
        self.customer_controller = customer_controller
        self.warehouse_controller = warehouse_controller
        self.financial_controller = financial_controller
        self.admin_controller = admin_controller
        self.manager_controller = manager_controller
        self.locations = self.warehouse_controller.get_all_locations()
        self.departments = self.auth_controller.get_all_departments()
        self.permissions = self.auth_controller.get_all_permissions()

        # Initialize the main window with ttkbootstrap style
        self.style = Style(theme='cosmo')
        self.root = self.style.master
        self.root.title("E-Shop Management System")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_widgets()

    def create_widgets(self):
        self.login_frame = ttk.Frame(self.root, padding="10")
        self.login_frame.pack(padx=10, pady=10)

        self.username_label = ttk.Label(self.login_frame, text="Username")
        self.username_label.pack(pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(self.login_frame, text="Password")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        self.register_button = ttk.Button(self.login_frame, text="Register", command=self.register)
        self.register_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.auth_controller.authenticate_user(username, password)
        if user:
            self.show_notification("Login successful", "green")
            self.show_dashboard(user)
        else:
            self.show_notification("Invalid credentials", "red")

    def show_notification(self, message, color):
        notification = tk.Toplevel(self.root)
        notification.title("Notification")
        ttk.Label(notification, text=message, foreground=color).pack(pady=10)
        ttk.Button(notification, text="OK", command=notification.destroy).pack(pady=10)

    def register(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Register")

        ttk.Label(register_window, text="Username").pack(pady=5)
        username_entry = ttk.Entry(register_window)
        username_entry.pack(pady=5)

        ttk.Label(register_window, text="Email").pack(pady=5)
        email_entry = ttk.Entry(register_window)
        email_entry.pack(pady=5)

        ttk.Label(register_window, text="Password").pack(pady=5)
        password_entry = ttk.Entry(register_window, show="*")
        password_entry.pack(pady=5)

        ttk.Label(register_window, text="Role").pack(pady=5)
        role_var = tk.StringVar()
        role_dropdown = ttk.Combobox(register_window, textvariable=role_var)
        role_dropdown['values'] = ('customer', 'manager', 'admin')
        role_dropdown.pack(pady=5)

        ttk.Label(register_window, text="Date of Birth (YYYY-MM-DD)").pack(pady=5)
        dob_entry = ttk.Entry(register_window)
        dob_entry.pack(pady=5)

        def submit_registration():
            username = username_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            role = role_var.get()
            dob = dob_entry.get()

            # Validate email
            if not validate_email(email):
                self.show_notification("Invalid email address", "red")
                return

            # Validate date of birth
            try:
                datetime.strptime(dob, '%Y-%m-%d')
            except ValueError:
                self.show_notification("Invalid date format. Use YYYY-MM-DD", "red")
                return

            # Validate other fields
            if not username or not password or not role:
                self.show_notification("All fields are required", "red")
                return

            user = self.auth_controller.register_user(username, email, password, role)
            if user:
                self.show_notification("Registration successful", "green")
                register_window.destroy()
                self.prompt_additional_info(user)
            else:
                self.show_notification("Registration failed", "red")

        ttk.Button(register_window, text="Submit", command=submit_registration).pack(pady=10)

    def prompt_additional_info(self, user):
        additional_info_window = tk.Toplevel(self.root)
        additional_info_window.title("Additional Information")

        if user.role == "customer":
            ttk.Label(additional_info_window, text="Name").pack(pady=5)
            name_entry = ttk.Entry(additional_info_window)
            name_entry.pack(pady=5)

            ttk.Label(additional_info_window, text="Last Name").pack(pady=5)
            last_name_entry = ttk.Entry(additional_info_window)
            last_name_entry.pack(pady=5)

            ttk.Label(additional_info_window, text="Phone Number").pack(pady=5)
            phone_entry = ttk.Entry(additional_info_window)
            phone_entry.pack(pady=5)

            ttk.Label(additional_info_window, text="Address").pack(pady=5)
            address_entry = ttk.Entry(additional_info_window)
            address_entry.pack(pady=5)

            def submit_additional_info():
                name = name_entry.get()
                last_name = last_name_entry.get()
                phone = phone_entry.get()
                address = address_entry.get()

                if not name or not last_name or not phone or not address:
                    self.show_notification("All fields are required", "red")
                    return

                customer = self.auth_controller.register_user_additional(user=user, name=name, last_name=last_name, address=address, phone=phone, role=user.role)
                if customer:
                    self.show_notification("Customer information added successfully", "green")
                    additional_info_window.destroy()
                else:
                    self.show_notification("Failed to add customer information", "red")

            ttk.Button(additional_info_window, text="Submit", command=submit_additional_info).pack(pady=10)

        elif user.role == "manager":
            ttk.Label(additional_info_window, text="Location").pack(pady=5)
            location_var = tk.StringVar()
            location_entry = ttk.Combobox(additional_info_window, textvariable=location_var)
            location_entry['values'] = self.locations
            location_entry.pack(pady=5)

            ttk.Label(additional_info_window, text="Permissions").pack(pady=5)
            permissions_var = tk.StringVar()
            permissions_entry = ttk.Combobox(additional_info_window, textvariable=permissions_var)
            permissions_entry['values'] = self.permissions
            permissions_entry.pack(pady=5)

            def submit_additional_info():
                location = location_var.get()
                permissions = permissions_var.get()

                if not location or not permissions:
                    self.show_notification("All fields are required", "red")
                    return

                manager = self.auth_controller.register_user_additional(user=user, location=location, permissions=permissions, role=user.role)
                if manager:
                    self.show_notification("Manager information added successfully", "green")
                    additional_info_window.destroy()
                else:
                    self.show_notification("Failed to add manager information", "red")

            ttk.Button(additional_info_window, text="Submit", command=submit_additional_info).pack(pady=10)

        elif user.role == "admin":
            ttk.Label(additional_info_window, text="Department").pack(pady=5)
            department_var = tk.StringVar()
            department_entry = ttk.Combobox(additional_info_window, textvariable=department_var)
            department_entry['values'] = self.departments
            department_entry.pack(pady=5)

            ttk.Label(additional_info_window, text="Permissions").pack(pady=5)
            permissions_var = tk.StringVar()
            permissions_entry = ttk.Combobox(additional_info_window, textvariable=permissions_var)
            permissions_entry['values'] = self.permissions
            permissions_entry.pack(pady=5)

            def submit_additional_info():
                department = department_var.get()
                permissions = permissions_var.get()

                if not department or not permissions:
                    self.show_notification("All fields are required", "red")
                    return

                admin = self.auth_controller.register_user_additional(user=user, department=department, permissions=permissions, role=user.role)
                if admin:
                    self.show_notification("Admin information added successfully", "green")
                    additional_info_window.destroy()
                else:
                    self.show_notification("Failed to add admin information", "red")

            ttk.Button(additional_info_window, text="Submit", command=submit_additional_info).pack(pady=10)

    def show_dashboard(self, user):
        self.login_frame.pack_forget()
        self.dashboard_frame = ttk.Frame(self.root, padding="10")
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(self.dashboard_frame)

        if user.role == "admin":
            self.create_product_tab(notebook)
            self.create_order_tab(notebook)
            self.create_customer_tab(notebook)
            self.create_warehouse_tab(notebook)
            self.create_financial_tab(notebook)
        elif user.role == "manager":
            self.create_order_tab(notebook)
            self.create_warehouse_manager_tab(notebook, user.id)
        elif user.role == "customer":
            self.create_customer_dashboard(notebook, user)

        notebook.pack(fill=tk.BOTH, expand=True)

        self.logout_button = ttk.Button(self.dashboard_frame, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

    def create_product_tab(self, notebook):
        product_frame = ttk.Frame(notebook, padding="10")
        notebook.add(product_frame, text="Manage Products")
        ProductView(product_frame, self.product_controller, self.warehouse_controller)

    def create_order_tab(self, notebook):
        order_frame = ttk.Frame(notebook, padding="10")
        notebook.add(order_frame, text="Manage Orders")
        OrderView(order_frame, self.order_controller)

    def create_customer_tab(self, notebook):
        customer_frame = ttk.Frame(notebook, padding="10")
        notebook.add(customer_frame, text="Manage Customers")
        CustomerManager(customer_frame, self.customer_controller, self.order_controller)

    def create_warehouse_tab(self, notebook):
        warehouse_frame = ttk.Frame(notebook, padding="10")
        notebook.add(warehouse_frame, text="Manage Warehouses")
        WarehouseView(warehouse_frame, self.warehouse_controller)

    def create_financial_tab(self, notebook):
        financial_frame = ttk.Frame(notebook, padding="10")
        notebook.add(financial_frame, text="Manage Financials")
        FinancialView(financial_frame, self.financial_controller)

    def create_customer_dashboard(self, notebook, user):
        customer_dashboard_frame = ttk.Frame(notebook, padding="10")
        notebook.add(customer_dashboard_frame, text="Customer Dashboard")
        CustomerDashboard(customer_dashboard_frame, self.product_controller, self.order_controller, self.customer_controller, user)

    def create_warehouse_manager_tab(self, notebook, user_id):
        warehouse_manager_frame = ttk.Frame(notebook, padding="10")
        notebook.add(warehouse_manager_frame, text="Manage Warehouses")
        WarehouseManagerView(warehouse_manager_frame, self.warehouse_controller, self.manager_controller, user_id, self.product_controller, self.financial_controller, self.email_controller)

    def logout(self):
        self.dashboard_frame.pack_forget()
        self.create_widgets()

    def on_closing(self):
        self.root.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()