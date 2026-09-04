import threading

from django.utils import timezone

from .models import Product


def inventory_check_task():
    """
    Background task that checks product stock
    and updates the Product database table.
    """

    products = Product.objects.all()

    for product in products:

        if product.quantity_in_stock <= product.reorder_level:

            product.stock_status = "LOW STOCK"

        else:

            product.stock_status = "NORMAL"

        product.last_checked = timezone.now()

        product.save(
            update_fields=[
                "stock_status",
                "last_checked"
            ]
        )


def start_inventory_check():
    """
    Start the inventory check in a background thread.
    """

    thread = threading.Thread(
        target=inventory_check_task
    )

    thread.daemon = True

    thread.start()

    return thread