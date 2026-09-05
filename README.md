# Inventory Management System

## 1. Project Description

The Inventory Management System is a web-based application developed to manage products, suppliers, purchase orders, order items, and stock transactions.

The system provides a simple web interface and REST API for performing CRUD operations and managing inventory information efficiently.

## 2. Objectives

The main objectives of this project are:

- To manage supplier information.
- To manage product and stock information.
- To manage purchase orders and order items.
- To record stock-in and stock-out transactions.
- To provide related-entity and complex database queries.
- To provide a web-based graphical user interface.
- To provide REST API endpoints.
- To use Django ORM for database operations.
- To use Oracle Database for data storage.
- To implement inventory checking and stock status updates.

## 3. Technologies Used

- **Programming Language:** Python
- **Web Framework:** Django
- **API Framework:** Django REST Framework
- **Database:** Oracle Database
- **ORM:** Django ORM
- **Frontend:** HTML, CSS
- **Development Environment:** Visual Studio Code
- **Version Control:** Git and GitHub

## 4. System Features

### Supplier Management
- Add suppliers
- View suppliers
- Update supplier information
- Delete suppliers

### Product Management
- Add products
- View products
- Update products
- Delete products
- Monitor stock quantity
- Check reorder level and stock status

### Purchase Order Management
- Create purchase orders
- View purchase orders
- Manage order items
- Calculate order totals

### Stock Management
- Record stock-in transactions
- Record stock-out transactions
- View stock movement
- Monitor inventory levels

### Reports and Queries
The system supports queries involving related entities, including:

- Products supplied by a supplier
- Orders placed with a supplier
- Product stock transactions
- Purchase order details
- Stock movement information

### REST API
The application provides REST API endpoints for:

- Suppliers
- Products
- Purchase Orders
- Order Items
- Stock Transactions

## 5. Database Design

The system uses the following main tables:

1. `SUPPLIERS`
2. `PRODUCTS`
3. `PURCHASE_ORDERS`
4. `ORDER_ITEMS`
5. `STOCK_TRANSACTIONS`

Main relationships include:

- One Supplier can have many Products.
- One Supplier can have many Purchase Orders.
- One Purchase Order can contain many Order Items.
- One Product can appear in many Order Items.
- One Product can have many Stock Transactions.

## 6. Project Structure

```text
inventory-management-system/
│
├── inventory/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services.py
│   ├── urls.py
│   └── ...
│
├── inventory_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── templates/
│
├── static/
│
├── database/
│   └── inventory_schema.sql
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
