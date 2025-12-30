from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items."""
    product_image = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_sku', 'quantity', 
                  'unit_price', 'total_price', 'product_image']
        read_only_fields = ['id', 'product_name', 'product_sku', 'total_price']
    
    def get_product_image(self, obj):
        if obj.product:
            return obj.product.image_url or (obj.product.image.url if obj.product.image else None)
        return None


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders."""
    
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'email', 'first_name', 'last_name', 'phone',
            'shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip',
            'shipping_country', 'subtotal', 'shipping_cost', 'tax', 'total',
            'status', 'status_display', 'payment_status', 'payment_status_display',
            'payment_method', 'tracking_number', 'estimated_delivery',
            'notes', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_number', 'subtotal', 'total', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating an order."""
    
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    shipping_address = serializers.CharField()
    shipping_city = serializers.CharField(max_length=100)
    shipping_state = serializers.CharField(max_length=100)
    shipping_zip = serializers.CharField(max_length=20)
    shipping_country = serializers.CharField(max_length=100, default='India')
    notes = serializers.CharField(required=False, allow_blank=True)
    
    # Payment fields
    payment_method = serializers.ChoiceField(
        choices=['stripe', 'cod'],
        default='stripe'
    )
    stripe_payment_intent_id = serializers.CharField(required=False, allow_blank=True)


class OrderListSerializer(serializers.ModelSerializer):
    """Serializer for order list view."""
    
    items_count = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'total', 'status', 'status_display',
            'payment_status', 'payment_status_display', 'payment_method',
            'tracking_number', 'estimated_delivery', 'items_count', 'created_at'
        ]
    
    def get_items_count(self, obj):
        return obj.items.count()


class AdminOrderSerializer(serializers.ModelSerializer):
    """Serializer for admin order management."""
    
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    customer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer_name', 'email', 'first_name', 'last_name', 'phone',
            'shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip',
            'shipping_country', 'subtotal', 'shipping_cost', 'tax', 'total',
            'status', 'status_display', 'payment_status', 'payment_status_display',
            'payment_method', 'stripe_payment_intent_id',
            'tracking_number', 'estimated_delivery', 'notes', 'admin_notes',
            'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_number', 'subtotal', 'total', 'created_at', 'updated_at',
                           'stripe_payment_intent_id']
    
    def get_customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class OrderStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating order status."""
    
    status = serializers.ChoiceField(
        choices=Order.STATUS_CHOICES,
        required=False
    )
    payment_status = serializers.ChoiceField(
        choices=Order.PAYMENT_STATUS_CHOICES,
        required=False
    )
    tracking_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    estimated_delivery = serializers.DateField(required=False, allow_null=True)
    admin_notes = serializers.CharField(required=False, allow_blank=True)
