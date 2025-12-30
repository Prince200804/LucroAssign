from rest_framework import serializers
from .models import ProductInteraction, DailyProductStats, DailyCategoryStats, UserBehaviorSummary
from products.serializers import ProductListSerializer, CategorySerializer


class ProductInteractionSerializer(serializers.ModelSerializer):
    """Serializer for product interactions."""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True, default=None)
    
    class Meta:
        model = ProductInteraction
        fields = [
            'id', 'product', 'product_name', 'user', 'user_email',
            'session_key', 'interaction_type', 'metadata', 'ip_address',
            'created_at'
        ]


class DailyProductStatsSerializer(serializers.ModelSerializer):
    """Serializer for daily product stats."""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_category = serializers.CharField(source='product.category.name', read_only=True)
    
    class Meta:
        model = DailyProductStats
        fields = [
            'id', 'product', 'product_name', 'product_category', 'date',
            'views', 'clicks', 'add_to_cart', 'remove_from_cart',
            'purchases', 'revenue', 'unique_visitors'
        ]


class DailyCategoryStatsSerializer(serializers.ModelSerializer):
    """Serializer for daily category stats."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = DailyCategoryStats
        fields = [
            'id', 'category', 'category_name', 'date',
            'views', 'clicks', 'add_to_cart', 'purchases', 'revenue'
        ]


class UserBehaviorSummarySerializer(serializers.ModelSerializer):
    """Serializer for user behavior summary."""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True, default=None)
    
    class Meta:
        model = UserBehaviorSummary
        fields = [
            'id', 'user', 'user_email', 'session_key', 'product', 'product_name',
            'viewed', 'clicked', 'added_to_cart', 'removed_from_cart', 'purchased',
            'view_count', 'cart_add_count', 'cart_remove_count', 'purchase_count',
            'first_view_at', 'last_view_at', 'purchased_at'
        ]


# Analytics Summary Serializers
class ProductAnalyticsSummarySerializer(serializers.Serializer):
    """Summary analytics for a product."""
    
    product_id = serializers.UUIDField()
    product_name = serializers.CharField()
    product_image = serializers.CharField(allow_null=True)
    category_name = serializers.CharField()
    total_views = serializers.IntegerField()
    total_clicks = serializers.IntegerField()
    total_add_to_cart = serializers.IntegerField()
    total_remove_from_cart = serializers.IntegerField()
    total_purchases = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    conversion_rate = serializers.FloatField()


class CategoryAnalyticsSummarySerializer(serializers.Serializer):
    """Summary analytics for a category."""
    
    category_id = serializers.UUIDField()
    category_name = serializers.CharField()
    total_views = serializers.IntegerField()
    total_add_to_cart = serializers.IntegerField()
    total_purchases = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    product_count = serializers.IntegerField()


class TimeSeriesDataSerializer(serializers.Serializer):
    """Time series data point."""
    
    date = serializers.DateField()
    views = serializers.IntegerField()
    add_to_cart = serializers.IntegerField()
    purchases = serializers.IntegerField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)


class FunnelDataSerializer(serializers.Serializer):
    """Funnel analysis data."""
    
    stage = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.FloatField()


class TrackInteractionSerializer(serializers.Serializer):
    """Serializer for tracking interactions from frontend."""
    
    product_id = serializers.UUIDField()
    interaction_type = serializers.ChoiceField(choices=[
        'view', 'click', 'add_to_cart', 'remove_from_cart', 'purchase'
    ])
    metadata = serializers.DictField(required=False, default=dict)
