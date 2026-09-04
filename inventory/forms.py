from django import forms

from .models import (
    Supplier,
    Product,
    PurchaseOrder,
    OrderItem,
    StockTransaction,
)


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = [
            "supplier_name",
            "phone",
            "email",
            "address",
        ]


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            "product_name",
            "category",
            "unit_price",
            "quantity_in_stock",
            "reorder_level",
            "supplier",
        ]


class PurchaseOrderForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        fields = [
            "supplier",
            "status",
        ]


class OrderItemForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = [
            "order",
            "product",
            "quantity",
            "unit_price",
        ]


class StockTransactionForm(forms.ModelForm):

    class Meta:
        model = StockTransaction
        fields = [
            "product",
            "transaction_type",
            "quantity",
            "reference",
            "remarks",
        ]