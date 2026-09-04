from django.db import models
from django.core.validators import MinValueValidator


class Supplier(models.Model):
    supplier_id = models.BigAutoField(primary_key=True)

    supplier_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        max_length=150,
        unique=True
    )

    address = models.CharField(
        max_length=255
    )

    class Meta:
        db_table = "suppliers"
        ordering = ["supplier_name"]

    def __str__(self):
        return self.supplier_name


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)

    product_name = models.CharField(
        max_length=150
    )

    category = models.CharField(
        max_length=100
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    quantity_in_stock = models.PositiveIntegerField(
        default=0
    )

    reorder_level = models.PositiveIntegerField(
        default=10
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="products"
    )

    class Meta:
        db_table = "products"
        ordering = ["product_name"]

    def __str__(self):
        return self.product_name

    @property
    def is_low_stock(self):
        return self.quantity_in_stock <= self.reorder_level
    
    stock_status = models.CharField(
    max_length=20,
    default="NORMAL"
    )

    last_checked = models.DateTimeField(
    null=True,
    blank=True
    )


class PurchaseOrder(models.Model):

    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        RECEIVED = "RECEIVED", "Received"
        CANCELLED = "CANCELLED", "Cancelled"

    order_id = models.BigAutoField(
        primary_key=True
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="purchase_orders"
    )

    order_date = models.DateField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = "purchase_orders"
        ordering = ["-order_date", "-order_id"]

    def __str__(self):
        return f"PO-{self.order_id}"


class OrderItem(models.Model):

    order_item_id = models.BigAutoField(
        primary_key=True
    )

    order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items"
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    subtotal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = "order_items"

        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"],
                name="unique_order_product"
            )
        ]

    def save(self, *args, **kwargs):

        self.subtotal = (
            self.quantity * self.unit_price
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.quantity}"


class StockTransaction(models.Model):

    class TransactionType(models.TextChoices):
        STOCK_IN = "STOCK_IN", "Stock In"
        STOCK_OUT = "STOCK_OUT", "Stock Out"
        ADJUSTMENT = "ADJUSTMENT", "Adjustment"

    transaction_id = models.BigAutoField(
        primary_key=True
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="stock_transactions"
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    transaction_date = models.DateTimeField(
        auto_now_add=True
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    remarks = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        db_table = "stock_transactions"
        ordering = ["-transaction_date"]

    def __str__(self):
        return (
            f"{self.product} - "
            f"{self.transaction_type} - "
            f"{self.quantity}"
        )
