from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_sku', 'unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'email', 'total', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'email', 'first_name', 'last_name']
    readonly_fields = ['order_number', 'subtotal', 'total', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    list_editable = ['status', 'payment_status']
