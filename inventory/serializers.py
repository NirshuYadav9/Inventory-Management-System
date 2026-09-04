from rest_framework import serializers

from .models import (
    Supplier,
    Product,
    PurchaseOrder,
    OrderItem,
    StockTransaction,
)


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            "supplier_id",
            "supplier_name",
            "phone",
            "email",
            "address",
        ]
        read_only_fields = ["supplier_id"]


class ProductSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(
        source="supplier.supplier_name",
        read_only=True
    )

    is_low_stock = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "product_id",
            "product_name",
            "category",
            "unit_price",
            "quantity_in_stock",
            "reorder_level",
            "supplier",
            "supplier_name",
            "is_low_stock",
        ]
        read_only_fields = [
            "product_id",
            "is_low_stock",
        ]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(
        source="supplier.supplier_name",
        read_only=True
    )

    class Meta:
        model = PurchaseOrder
        fields = [
            "order_id",
            "supplier",
            "supplier_name",
            "order_date",
            "status",
            "total_amount",
        ]
        read_only_fields = [
            "order_id",
            "order_date",
            "total_amount",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.product_name",
        read_only=True
    )

    subtotal = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "order_item_id",
            "order",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "subtotal",
        ]
        read_only_fields = [
            "order_item_id",
            "subtotal",
        ]


class StockTransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.product_name",
        read_only=True
    )

    class Meta:
        model = StockTransaction
        fields = [
            "transaction_id",
            "product",
            "product_name",
            "transaction_type",
            "quantity",
            "transaction_date",
            "reference",
            "remarks",
        ]
        read_only_fields = [
            "transaction_id",
            "transaction_date",
        ]