from django.db import models
from django.conf import settings
from products.models import Product, Category
import uuid


class ProductInteraction(models.Model):
    """Track all product interactions."""
    
    INTERACTION_TYPES = [
        ('view', 'Product View'),
        ('click', 'Product Click'),
        ('add_to_cart', 'Added to Cart'),
        ('remove_from_cart', 'Removed from Cart'),
        ('purchase', 'Purchased'),
        ('wishlist_add', 'Added to Wishlist'),
        ('wishlist_remove', 'Removed from Wishlist'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interactions'
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'product_interactions'
        verbose_name = 'Product Interaction'
        verbose_name_plural = 'Product Interactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', 'interaction_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user']),
            models.Index(fields=['session_key']),
        ]
    
    def __str__(self):
        user_info = self.user.email if self.user else f"Anonymous ({self.session_key[:8]}...)" if self.session_key else "Unknown"
        return f"{self.interaction_type} - {self.product.name} by {user_info}"


class DailyProductStats(models.Model):
    """Aggregated daily statistics per product."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='daily_stats')
    date = models.DateField()
    views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    add_to_cart = models.PositiveIntegerField(default=0)
    remove_from_cart = models.PositiveIntegerField(default=0)
    purchases = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'daily_product_stats'
        unique_together = ['product', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.product.name} - {self.date}"


class DailyCategoryStats(models.Model):
    """Aggregated daily statistics per category."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='daily_stats')
    date = models.DateField()
    views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    add_to_cart = models.PositiveIntegerField(default=0)
    purchases = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    class Meta:
        db_table = 'daily_category_stats'
        unique_together = ['category', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.category.name} - {self.date}"


class UserBehaviorSummary(models.Model):
    """Track user journey and behavior patterns."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # Behavior flags
    viewed = models.BooleanField(default=False)
    clicked = models.BooleanField(default=False)
    added_to_cart = models.BooleanField(default=False)
    removed_from_cart = models.BooleanField(default=False)
    purchased = models.BooleanField(default=False)
    
    # Timestamps
    first_view_at = models.DateTimeField(null=True, blank=True)
    last_view_at = models.DateTimeField(null=True, blank=True)
    added_to_cart_at = models.DateTimeField(null=True, blank=True)
    removed_from_cart_at = models.DateTimeField(null=True, blank=True)
    purchased_at = models.DateTimeField(null=True, blank=True)
    
    # Counts
    view_count = models.PositiveIntegerField(default=0)
    cart_add_count = models.PositiveIntegerField(default=0)
    cart_remove_count = models.PositiveIntegerField(default=0)
    purchase_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_behavior_summary'
        unique_together = [['user', 'product'], ['session_key', 'product']]
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['viewed', 'purchased']),
            models.Index(fields=['added_to_cart', 'purchased']),
        ]
    
    def __str__(self):
        user_info = self.user.email if self.user else f"Session {self.session_key[:8]}"
        return f"{user_info} - {self.product.name}"
