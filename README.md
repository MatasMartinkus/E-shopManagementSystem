# E-Shop Management System

## Project Overview
The E-Shop Management System is a comprehensive solution for managing online retail operations. It provides features for inventory management, order processing, customer management, and sales analytics.

## Features
- Inventory Management
- Order Processing
- Customer Management
- Sales Analytics
- User Authentication and Authorization

## Installation
To install the E-Shop Management System, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/MatasMartinkus/E-shopManagementSystem.git
    ```
2. Navigate to the project directory:
    ```bash
    cd eshop-management-system
    ```
3. Create a virtual environment:
    ```bash
    python -m venv .venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```bash
        .venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```
5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## PostgreSQL Setup
The E-Shop Management System uses PostgreSQL as its database. Follow these steps to set up PostgreSQL:
1. Install PostgreSQL from the official website: [PostgreSQL Downloads](https://www.postgresql.org/download/)
2. Create a new database and user:
    ```sql
    CREATE DATABASE eshop_db;
    CREATE USER eshop_user WITH ENCRYPTED PASSWORD 'yourpassword';
    GRANT ALL PRIVILEGES ON DATABASE eshop_db TO eshop_user;
    ```
3. Update the `DATABASE_URL` in the `.env` file with your PostgreSQL connection details:
    ```
    DATABASE_URL=postgresql://eshop_user:yourpassword@localhost:5432/eshop_db
    ```

## Usage
To start the application, run the following command:
```bash
python manage.py runserver
```
Open your web browser and navigate to `http://localhost:8000` to access the application.

## Database Schema
The E-Shop Management System uses a relational database to manage its data. Below is a high-level overview of the database schema:

### User
- `id`: Integer, Primary Key
- `username`: String, Unique
- `email`: String, Unique
- `hashed_password`: String
- `is_verified`: Boolean
- `role`: String

### Customer
- `id`: Integer, Primary Key
- `user_id`: Integer, Foreign Key (references User)
- `name`: String
- `last_name`: String
- `phone`: String
- `address`: String
- `reference_code`: String, Unique

### Product
- `id`: Integer, Primary Key
- `warehouse_id`: Integer, Foreign Key (references Warehouse)
- `name`: String
- `description`: String
- `price`: Float
- `stock_quantity`: Integer
- `category`: String
- `subcategory`: String
- `length`: Float
- `width`: Float
- `height`: Float
- `weight`: Float

### Order
- `id`: Integer, Primary Key
- `customer_id`: Integer, Foreign Key (references Customer)
- `date_created`: DateTime

### OrderProduct
- `id`: Integer, Primary Key
- `order_id`: Integer, Foreign Key (references Order)
- `product_id`: Integer, Foreign Key (references Product)
- `name`: String
- `price`: Float
- `quantity`: Integer

### Warehouse
- `id`: Integer, Primary Key
- `location`: String
- `capacity`: Integer
- `max_volume`: Float
- `max_weight`: Float
- `current_volume`: Float
- `current_weight`: Float

### Financial
- `id`: Integer, Primary Key
- `transaction_date`: DateTime
- `amount`: Float
- `transaction_type`: String
- `recipient`: String
- `sender`: String

### Graphs
Below are the graphical representations of the database relationships:

![Database Relationships](images/database_relationships.png)

## Use Cases
The E-Shop Management System can be used in various scenarios:
- **Retail Stores**: Manage inventory, process orders, and analyze sales data.
- **E-commerce Platforms**: Handle customer information, track orders, and manage product listings.
- **Warehouse Management**: Monitor stock levels, manage warehouse space, and track product movements.

## Main Functionalities
- **Inventory Management**: Keep track of product stock levels, manage warehouse space, and update product information.
- **Order Processing**: Handle customer orders, manage order statuses, and generate invoices.
- **Customer Management**: Store customer information, manage customer accounts, and track customer orders.
- **Sales Analytics**: Generate sales reports, analyze sales data, and track sales performance.
- **User Authentication and Authorization**: Secure user login, manage user roles, and verify user accounts.

