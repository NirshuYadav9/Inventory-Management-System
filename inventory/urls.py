from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    # API ViewSets
    SupplierViewSet,
    ProductViewSet,
    PurchaseOrderViewSet,
    OrderItemViewSet,
    StockTransactionViewSet,

    dashboard,

    # ...your existing imports...

    run_inventory_check,

    # Dashboard
    dashboard,

    # Supplier GUI
    supplier_list,
    supplier_create,
    supplier_update,
    supplier_delete,

    # Product GUI
    product_list,
    product_create,
    product_update,
    product_delete,
    low_stock,

    # Purchase Order GUI
    purchase_order_list,
    purchase_order_create,

    # Stock GUI
    stock_transaction_list,
    stock_transaction_create,

    # Part 4 queries
    products_by_supplier,
    orders_by_supplier,
    transactions_by_product,
    purchase_details,
    stock_movement_report,
)


# ============================================================
# API ROUTER
# ============================================================

router = DefaultRouter()

router.register(
    r"suppliers",
    SupplierViewSet,
    basename="supplier"
)

router.register(
    r"products",
    ProductViewSet,
    basename="product"
)

router.register(
    r"purchase-orders",
    PurchaseOrderViewSet,
    basename="purchase-order"
)

router.register(
    r"order-items",
    OrderItemViewSet,
    basename="order-item"
)

router.register(
    r"stock-transactions",
    StockTransactionViewSet,
    basename="stock-transaction"
)


# ============================================================
# URL PATTERNS
# ============================================================

urlpatterns = [

    # --------------------------------------------------------
    # WEB GUI
    # --------------------------------------------------------

    path(
        "",
        dashboard,
        name="dashboard"
    ),

    # Suppliers
    path(
        "suppliers/",
        supplier_list,
        name="supplier_list"
    ),

    path(
        "suppliers/add/",
        supplier_create,
        name="supplier_create"
    ),

    path(
        "suppliers/<int:pk>/edit/",
        supplier_update,
        name="supplier_update"
    ),

    path(
        "suppliers/<int:pk>/delete/",
        supplier_delete,
        name="supplier_delete"
    ),

    # Products
    path(
        "products/",
        product_list,
        name="product_list"
    ),

    path(
        "products/add/",
        product_create,
        name="product_create"
    ),

    path(
        "products/<int:pk>/edit/",
        product_update,
        name="product_update"
    ),

    path(
        "products/<int:pk>/delete/",
        product_delete,
        name="product_delete"
    ),

    path(
        "products/low-stock/",
        low_stock,
        name="low_stock"
    ),

    # Purchase Orders
    path(
        "purchase-orders/",
        purchase_order_list,
        name="purchase_order_list"
    ),

    path(
        "purchase-orders/add/",
        purchase_order_create,
        name="purchase_order_create"
    ),

    # Stock
    path(
        "stock/",
        stock_transaction_list,
        name="stock_transaction_list"
    ),

    path(
        "stock/add/",
        stock_transaction_create,
        name="stock_transaction_create"
    ),

    path(
        "inventory-check/",
        run_inventory_check,
        name="run_inventory_check"
    ),

    # --------------------------------------------------------
    # PART 4 — RELATED ENTITY QUERIES
    # --------------------------------------------------------

    path(
        "reports/supplier/<int:supplier_id>/products/",
        products_by_supplier,
        name="products_by_supplier"
    ),

    path(
        "reports/supplier/<int:supplier_id>/orders/",
        orders_by_supplier,
        name="orders_by_supplier"
    ),

    path(
        "reports/product/<int:product_id>/transactions/",
        transactions_by_product,
        name="transactions_by_product"
    ),

    # --------------------------------------------------------
    # PART 4 — COMPLEX QUERIES
    # --------------------------------------------------------

    path(
        "reports/purchase-details/",
        purchase_details,
        name="purchase_details"
    ),

    path(
        "reports/stock-movement/",
        stock_movement_report,
        name="stock_movement_report"
    ),

    # --------------------------------------------------------
    # REST API
    # --------------------------------------------------------

    path(
        "api/",
        include(router.urls)
    ),
]