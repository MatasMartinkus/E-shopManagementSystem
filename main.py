from flask import Flask
from src.gui.main_window import MainWindow
from src.utils.dbengine import initialize_db
from src.controllers.email_controller import EmailController
from src.controllers.auth_controller import AuthController
from src.controllers.product_controller import ProductController
from src.controllers.order_controller import OrderController
from src.controllers.customer_controller import CustomerController
from src.controllers.warehouse_controller import WarehouseController
from src.controllers.financial_controller import FinancialController
from src.controllers.admin_controller import AdminController
from src.controllers.manager_controller import ManagerController
import threading
import os
from dotenv import load_dotenv
import sys

def start_flask_app(app):
    app.run(port=5000)

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Initialize the database
    initialize_db()

    # Initialize Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # SMTP configuration
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    email_controller = EmailController(app, smtp_server, smtp_port, smtp_user, smtp_password)

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=start_flask_app, args=(app,))
    flask_thread.start()

    # Initialize controllers
    customer_controller = CustomerController()
    admin_controller = AdminController()
    manager_controller = ManagerController()
    auth_controller = AuthController(email_controller,customer_controller, admin_controller, manager_controller)
    product_controller = ProductController()
    order_controller = OrderController()
    warehouse_controller = WarehouseController()
    financial_controller = FinancialController()
    

    # Start the main GUI window
    main_window = MainWindow(auth_controller, product_controller, order_controller, warehouse_controller, financial_controller, admin_controller, manager_controller, customer_controller, email_controller)

    # Run the main GUI window
    try:
        main_window.run()
    except KeyboardInterrupt:
        print("Shutting down...")
        flask_thread.join()
        sys.exit(0)
    except exit:
        print("Shutting down...")
        flask_thread.join()
        sys.exit(0)

if __name__ == "__main__":
    main()