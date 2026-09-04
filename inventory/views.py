from .tasks import start_inventory_check
from django.db.models import F
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Supplier,
    Product,
    PurchaseOrder,
    OrderItem,
    StockTransaction,
)

from .serializers import (
    SupplierSerializer,
    ProductSerializer,
    PurchaseOrderSerializer,
    OrderItemSerializer,
    StockTransactionSerializer,
)

from .services import (
    SupplierService,
    ProductService,
    PurchaseOrderService,
    OrderItemService,
    StockTransactionService,
    ReportService,
)


# ============================================================
# SUPPLIER API
# ============================================================

class SupplierViewSet(viewsets.ViewSet):

    def list(self, request):

        suppliers = SupplierService.get_all()

        serializer = SupplierSerializer(
            suppliers,
            many=True
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            supplier = SupplierService.get_by_id(pk)

            serializer = SupplierSerializer(
                supplier
            )

            return Response(serializer.data)

        except Supplier.DoesNotExist:

            return Response(
                {"error": "Supplier not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):

        serializer = SupplierSerializer(
            data=request.data
        )

        if serializer.is_valid():

            supplier = SupplierService.create(
                serializer.validated_data
            )

            return Response(
                SupplierSerializer(supplier).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        serializer = SupplierSerializer(
            data=request.data
        )

        if serializer.is_valid():

            try:

                supplier = SupplierService.update(
                    pk,
                    serializer.validated_data
                )

                return Response(
                    SupplierSerializer(supplier).data
                )

            except Supplier.DoesNotExist:

                return Response(
                    {"error": "Supplier not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        try:

            SupplierService.delete(pk)

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        except Supplier.DoesNotExist:

            return Response(
                {"error": "Supplier not found."},
                status=status.HTTP_404_NOT_FOUND
            )


# ============================================================
# PRODUCT API
# ============================================================

class ProductViewSet(viewsets.ViewSet):

    def list(self, request):

        products = ProductService.get_all()

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:

            product = ProductService.get_by_id(pk)

            serializer = ProductSerializer(product)

            return Response(serializer.data)

        except Product.DoesNotExist:

            return Response(
                {"error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():

            product = ProductService.create(
                serializer.validated_data
            )

            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():

            try:

                product = ProductService.update(
                    pk,
                    serializer.validated_data
                )

                return Response(
                    ProductSerializer(product).data
                )

            except Product.DoesNotExist:

                return Response(
                    {"error": "Product not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        try:

            ProductService.delete(pk)

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        except Product.DoesNotExist:

            return Response(
                {"error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(
        detail=False,
        methods=["get"],
        url_path="low-stock"
    )
    def low_stock(self, request):

        products = (
            ProductService.get_low_stock_products()
        )

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)


# ============================================================
# PURCHASE ORDER API
# ============================================================

class PurchaseOrderViewSet(viewsets.ViewSet):

    def list(self, request):

        orders = PurchaseOrderService.get_all()

        serializer = PurchaseOrderSerializer(
            orders,
            many=True
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:

            order = PurchaseOrderService.get_by_id(pk)

            serializer = PurchaseOrderSerializer(order)

            return Response(serializer.data)

        except PurchaseOrder.DoesNotExist:

            return Response(
                {"error": "Purchase order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):

        serializer = PurchaseOrderSerializer(
            data=request.data
        )

        if serializer.is_valid():

            order = PurchaseOrderService.create(
                serializer.validated_data
            )

            return Response(
                PurchaseOrderSerializer(order).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        serializer = PurchaseOrderSerializer(
            data=request.data
        )

        if serializer.is_valid():

            try:

                order = PurchaseOrderService.update(
                    pk,
                    serializer.validated_data
                )

                return Response(
                    PurchaseOrderSerializer(order).data
                )

            except PurchaseOrder.DoesNotExist:

                return Response(
                    {"error": "Purchase order not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        try:

            PurchaseOrderService.delete(pk)

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        except PurchaseOrder.DoesNotExist:

            return Response(
                {"error": "Purchase order not found."},
                status=status.HTTP_404_NOT_FOUND
            )


# ============================================================
# ORDER ITEM API
# ============================================================

class OrderItemViewSet(viewsets.ViewSet):

    def list(self, request):

        items = OrderItemService.get_all()

        serializer = OrderItemSerializer(
            items,
            many=True
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:

            item = OrderItemService.get_by_id(pk)

            serializer = OrderItemSerializer(item)

            return Response(serializer.data)

        except OrderItem.DoesNotExist:

            return Response(
                {"error": "Order item not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):

        serializer = OrderItemSerializer(
            data=request.data
        )

        if serializer.is_valid():

            item = OrderItemService.create(
                serializer.validated_data
            )

            return Response(
                OrderItemSerializer(item).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):

        serializer = OrderItemSerializer(
            data=request.data
        )

        if serializer.is_valid():

            try:

                item = OrderItemService.update(
                    pk,
                    serializer.validated_data
                )

                return Response(
                    OrderItemSerializer(item).data
                )

            except OrderItem.DoesNotExist:

                return Response(
                    {"error": "Order item not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        try:

            OrderItemService.delete(pk)

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        except OrderItem.DoesNotExist:

            return Response(
                {"error": "Order item not found."},
                status=status.HTTP_404_NOT_FOUND
            )


# ============================================================
# STOCK TRANSACTION API
# ============================================================

class StockTransactionViewSet(viewsets.ViewSet):

    def list(self, request):

        transactions = (
            StockTransactionService.get_all()
        )

        serializer = StockTransactionSerializer(
            transactions,
            many=True
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:

            transaction = (
                StockTransactionService.get_by_id(pk)
            )

            serializer = StockTransactionSerializer(
                transaction
            )

            return Response(serializer.data)

        except StockTransaction.DoesNotExist:

            return Response(
                {"error": "Stock transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):

        serializer = StockTransactionSerializer(
            data=request.data
        )

        if serializer.is_valid():

            try:

                transaction = (
                    StockTransactionService.create(
                        serializer.validated_data
                    )
                )

                return Response(
                    StockTransactionSerializer(
                        transaction
                    ).data,
                    status=status.HTTP_201_CREATED
                )

            except ValueError as error:

                return Response(
                    {"error": str(error)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):

        try:

            StockTransactionService.delete(pk)

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        except StockTransaction.DoesNotExist:

            return Response(
                {"error": "Stock transaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )


# ============================================================
# WEB GUI VIEWS
# ============================================================

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import (
    SupplierForm,
    ProductForm,
    PurchaseOrderForm,
    OrderItemForm,
    StockTransactionForm,
)


def dashboard(request):

    context = {
        "supplier_count": Supplier.objects.count(),
        "product_count": Product.objects.count(),
        "order_count": PurchaseOrder.objects.count(),
        "low_stock_count": Product.objects.filter(
            quantity_in_stock__lte=F("reorder_level")
        ).count(),
    }

    return render(
        request,
        "inventory/dashboard.html",
        context
    )


# ============================================================
# SUPPLIERS
# ============================================================

def supplier_list(request):

    suppliers = SupplierService.get_all()

    return render(
        request,
        "inventory/supplier_list.html",
        {
            "suppliers": suppliers
        }
    )


def supplier_create(request):

    if request.method == "POST":

        form = SupplierForm(request.POST)

        if form.is_valid():

            SupplierService.create(
                form.cleaned_data
            )

            messages.success(
                request,
                "Supplier added successfully."
            )

            return redirect("supplier_list")

    else:

        form = SupplierForm()

    return render(
        request,
        "inventory/form.html",
        {
            "form": form,
            "title": "Add Supplier",
            "back_url": "supplier_list",
        }
    )


def supplier_update(request, pk):

    supplier = get_object_or_404(
        Supplier,
        supplier_id=pk
    )

    if request.method == "POST":

        form = SupplierForm(
            request.POST,
            instance=supplier
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Supplier updated successfully."
            )

            return redirect("supplier_list")

    else:

        form = SupplierForm(
            instance=supplier
        )

    return render(
        request,
        "inventory/form.html",
        {
            "form": form,
            "title": "Edit Supplier",
            "back_url": "supplier_list",
        }
    )


def supplier_delete(request, pk):

    supplier = get_object_or_404(
        Supplier,
        supplier_id=pk
    )

    if request.method == "POST":

        supplier.delete()

        messages.success(
            request,
            "Supplier deleted successfully."
        )

        return redirect("supplier_list")

    return render(
        request,
        "inventory/confirm_delete.html",
        {
            "object": supplier,
            "type": "Supplier",
            "back_url": "supplier_list",
        }
    )


# ============================================================
# PRODUCTS
# ============================================================

def product_list(request):

    products = ProductService.get_all()

    return render(
        request,
        "inventory/product_list.html",
        {
            "products": products
        }
    )


def product_create(request):

    if request.method == "POST":

        form = ProductForm(request.POST)

        if form.is_valid():

            ProductService.create(
                form.cleaned_data
            )

            messages.success(
                request,
                "Product added successfully."
            )

            return redirect("product_list")

    else:

        form = ProductForm()

    return render(
        request,
        "inventory/form.html",
        {
            "form": form,
            "title": "Add Product",
            "back_url": "product_list",
        }
    )


def product_update(request, pk):

    product = get_object_or_404(
        Product,
        product_id=pk
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect("product_list")

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        "inventory/form.html",
        {
            "form": form,
            "title": "Edit Product",
            "back_url": "product_list",
        }
    )


def product_delete(request, pk):

    product = get_object_or_404(
        Product,
        product_id=pk
    )

    if request.method == "POST":

        product.delete()

        messages.success(
            request,
            "Product deleted successfully."
        )

        return redirect("product_list")

    return render(
        request,
        "inventory/confirm_delete.html",
        {
            "object": product,
            "type": "Product",
            "back_url": "product_list",
        }
    )


def low_stock(request):

    products = ProductService.get_low_stock_products()

    return render(
        request,
        "inventory/low_stock.html",
        {
            "products": products
        }
    )


# ============================================================
# PURCHASE ORDERS
# ============================================================

def purchase_order_list(request):

    orders = PurchaseOrderService.get_all()

    return render(
        request,
        "inventory/purchase_order_list.html",
        {
            "orders": orders
        }
    )


def purchase_order_create(request):

    if request.method == "POST":

        form = PurchaseOrderForm(request.POST)

        if form.is_valid():

            PurchaseOrderService.create(
                form.cleaned_data
            )

            messages.success(
                request,
                "Purchase order created successfully."
            )

            return redirect(
                "purchase_order_list"
            )

    else:

        form = PurchaseOrderForm()

    return render(
        request,
        "inventory/form.html",
        {
            "form": form,
            "title": "Create Purchase Order",
            "back_url": "purchase_order_list",
        }
    )


# ============================================================
# STOCK TRANSACTIONS
# ============================================================

def stock_transaction_list(request):

    transactions = (
        StockTransactionService.get_all()
    )

    return render(
        request,
        "inventory/stock_transaction_list.html",
        {
            "transactions": transactions
        }
    )


def stock_transaction_create(request):

    if request.method == "POST":

        form = StockTransactionForm(
            request.POST
        )

        if form.is_valid():

            try:

                StockTransactionService.create(
                    form.cleaned_data
                )

                messages.success(
                    request,
                    "Stock transaction recorded successfully."
                )

                return redirect(
                    "stock_transaction_list"
                )

            except ValueError as error:

                form.add_error(
                    None,
                    str(error)
                )

    else:

        form = StockTransactionForm()

    return render(
        request,
        "inventory/form.html",
        {
            "form": form,
            "title": "Stock Transaction",
            "back_url": "stock_transaction_list",
        }
    )


# ============================================================
# RELATED ENTITY QUERY VIEWS
# ============================================================

def products_by_supplier(request, supplier_id):

    supplier = get_object_or_404(
        Supplier,
        supplier_id=supplier_id
    )

    products = ReportService.products_by_supplier(
        supplier_id
    )

    return render(
        request,
        "inventory/products_by_supplier.html",
        {
            "supplier": supplier,
            "products": products,
        }
    )


def orders_by_supplier(request, supplier_id):

    supplier = get_object_or_404(
        Supplier,
        supplier_id=supplier_id
    )

    orders = ReportService.orders_by_supplier(
        supplier_id
    )

    return render(
        request,
        "inventory/orders_by_supplier.html",
        {
            "supplier": supplier,
            "orders": orders,
        }
    )


def transactions_by_product(request, product_id):

    product = get_object_or_404(
        Product,
        product_id=product_id
    )

    transactions = (
        ReportService.transactions_by_product(
            product_id
        )
    )

    return render(
        request,
        "inventory/transactions_by_product.html",
        {
            "product": product,
            "transactions": transactions,
        }
    )


# ============================================================
# COMPLEX QUERY VIEWS
# ============================================================

def purchase_details(request):

    items = ReportService.purchase_details()

    return render(
        request,
        "inventory/purchase_details.html",
        {
            "items": items
        }
    )


def stock_movement_report(request):

    transactions = (
        ReportService.stock_movement_report()
    )

    return render(
        request,
        "inventory/stock_movement_report.html",
        {
            "transactions": transactions
        }
    )

def run_inventory_check(request):

    if request.method == "POST":

        start_inventory_check()

        messages.success(
            request,
            "Inventory check started in the background."
        )

        return redirect("dashboard")

    return redirect("dashboard")