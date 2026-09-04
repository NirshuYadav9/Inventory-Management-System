from decimal import Decimal

from django.db import transaction
from django.db.models import Sum, F

from .models import (
    Supplier,
    Product,
    PurchaseOrder,
    OrderItem,
    StockTransaction,
)


# ============================================================
# SUPPLIER SERVICE
# ============================================================

class SupplierService:

    @staticmethod
    def create(data):
        return Supplier.objects.create(**data)

    @staticmethod
    def get_all():
        return Supplier.objects.all()

    @staticmethod
    def get_by_id(supplier_id):
        return Supplier.objects.get(
            supplier_id=supplier_id
        )

    @staticmethod
    def update(supplier_id, data):
        supplier = Supplier.objects.get(
            supplier_id=supplier_id
        )

        for field, value in data.items():
            setattr(supplier, field, value)

        supplier.save()

        return supplier

    @staticmethod
    def delete(supplier_id):
        supplier = Supplier.objects.get(
            supplier_id=supplier_id
        )

        supplier.delete()


# ============================================================
# PRODUCT SERVICE
# ============================================================

class ProductService:

    @staticmethod
    def create(data):
        return Product.objects.create(**data)

    @staticmethod
    def get_all():
        return Product.objects.select_related(
            "supplier"
        ).all()

    @staticmethod
    def get_by_id(product_id):
        return Product.objects.select_related(
            "supplier"
        ).get(product_id=product_id)

    @staticmethod
    def update(product_id, data):
        product = Product.objects.get(
            product_id=product_id
        )

        for field, value in data.items():
            setattr(product, field, value)

        product.save()

        return product

    @staticmethod
    def delete(product_id):
        product = Product.objects.get(
            product_id=product_id
        )

        product.delete()

    @staticmethod
    def get_low_stock_products():
        return Product.objects.select_related(
            "supplier"
        ).filter(
            quantity_in_stock__lte=F("reorder_level")
        )


# ============================================================
# PURCHASE ORDER SERVICE
# ============================================================

class PurchaseOrderService:

    @staticmethod
    def create(data):
        return PurchaseOrder.objects.create(
            **data
        )

    @staticmethod
    def get_all():
        return PurchaseOrder.objects.select_related(
            "supplier"
        ).all()

    @staticmethod
    def get_by_id(order_id):
        return PurchaseOrder.objects.select_related(
            "supplier"
        ).get(order_id=order_id)

    @staticmethod
    def update(order_id, data):
        order = PurchaseOrder.objects.get(
            order_id=order_id
        )

        for field, value in data.items():
            setattr(order, field, value)

        order.save()

        return order

    @staticmethod
    def delete(order_id):
        order = PurchaseOrder.objects.get(
            order_id=order_id
        )

        order.delete()

    @staticmethod
    def calculate_total(order_id):

        result = OrderItem.objects.filter(
            order_id=order_id
        ).aggregate(
            total=Sum("subtotal")
        )

        total = result["total"] or Decimal("0.00")

        PurchaseOrder.objects.filter(
            order_id=order_id
        ).update(
            total_amount=total
        )

        return total


# ============================================================
# ORDER ITEM SERVICE
# ============================================================

class OrderItemService:

    @staticmethod
    @transaction.atomic
    def create(data):

        order = data["order"]
        product = data["product"]
        quantity = data["quantity"]

        item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            unit_price=product.unit_price
        )

        PurchaseOrderService.calculate_total(
            order.order_id
        )

        return item

    @staticmethod
    def get_all():
        return OrderItem.objects.select_related(
            "order",
            "product"
        ).all()

    @staticmethod
    def get_by_id(order_item_id):
        return OrderItem.objects.select_related(
            "order",
            "product"
        ).get(
            order_item_id=order_item_id
        )

    @staticmethod
    @transaction.atomic
    def update(order_item_id, data):

        item = OrderItem.objects.get(
            order_item_id=order_item_id
        )

        for field, value in data.items():
            setattr(item, field, value)

        if "product" in data and "unit_price" not in data:
            item.unit_price = data["product"].unit_price

        item.save()

        PurchaseOrderService.calculate_total(
            item.order.order_id
        )

        return item

    @staticmethod
    @transaction.atomic
    def delete(order_item_id):

        item = OrderItem.objects.get(
            order_item_id=order_item_id
        )

        order_id = item.order.order_id

        item.delete()

        PurchaseOrderService.calculate_total(
            order_id
        )


# ============================================================
# STOCK TRANSACTION SERVICE
# ============================================================

class StockTransactionService:

    @staticmethod
    @transaction.atomic
    def create(data):

        product = data["product"]
        transaction_type = data["transaction_type"]
        quantity = data["quantity"]

        if transaction_type == StockTransaction.TransactionType.STOCK_IN:

            product.quantity_in_stock += quantity

        elif transaction_type == StockTransaction.TransactionType.STOCK_OUT:

            if product.quantity_in_stock < quantity:
                raise ValueError(
                    "Insufficient stock available."
                )

            product.quantity_in_stock -= quantity

        elif transaction_type == StockTransaction.TransactionType.ADJUSTMENT:

            product.quantity_in_stock = quantity

        product.save()

        stock_transaction = StockTransaction.objects.create(
            **data
        )

        return stock_transaction

    @staticmethod
    def get_all():
        return StockTransaction.objects.select_related(
            "product"
        ).all()

    @staticmethod
    def get_by_id(transaction_id):
        return StockTransaction.objects.select_related(
            "product"
        ).get(
            transaction_id=transaction_id
        )

    @staticmethod
    def delete(transaction_id):
        transaction = StockTransaction.objects.get(
            transaction_id=transaction_id
        )

        transaction.delete()

# ============================================================
# REPORT / RELATED ENTITY QUERIES
# ============================================================

class ReportService:

    # --------------------------------------------------------
    # QUERY 1
    # Products supplied by a particular supplier
    # Supplier -> Product
    # --------------------------------------------------------

    @staticmethod
    def products_by_supplier(supplier_id):

        return Product.objects.select_related(
            "supplier"
        ).filter(
            supplier_id=supplier_id
        ).order_by(
            "product_name"
        )


    # --------------------------------------------------------
    # QUERY 2
    # Purchase orders belonging to a supplier
    # Supplier -> Purchase Order
    # --------------------------------------------------------

    @staticmethod
    def orders_by_supplier(supplier_id):

        return PurchaseOrder.objects.select_related(
            "supplier"
        ).filter(
            supplier_id=supplier_id
        ).order_by(
            "-order_date"
        )


    # --------------------------------------------------------
    # QUERY 3
    # Stock transactions for a product
    # Product -> Stock Transaction
    # --------------------------------------------------------

    @staticmethod
    def transactions_by_product(product_id):

        return StockTransaction.objects.select_related(
            "product"
        ).filter(
            product_id=product_id
        ).order_by(
            "-transaction_date"
        )


    # --------------------------------------------------------
    # COMPLEX QUERY 4
    #
    # Supplier -> Purchase Order
    #              ↓
    #          Order Item
    #              ↓
    #           Product
    #
    # Shows detailed purchase information.
    # --------------------------------------------------------

    @staticmethod
    def purchase_details():

        return OrderItem.objects.select_related(
            "order",
            "order__supplier",
            "product"
        ).order_by(
            "-order__order_date"
        )


    # --------------------------------------------------------
    # COMPLEX QUERY 5
    #
    # Product -> Supplier
    # Product -> Stock Transactions
    #
    # Shows stock movement with supplier information.
    # --------------------------------------------------------

    @staticmethod
    def stock_movement_report():

        return StockTransaction.objects.select_related(
            "product",
            "product__supplier"
        ).order_by(
            "-transaction_date"
        )