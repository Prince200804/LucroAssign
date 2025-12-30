from django.contrib import admin
from .models import ProductInteraction, DailyProductStats, DailyCategoryStats, UserBehaviorSummary


@admin.register(ProductInteraction)
class ProductInteractionAdmin(admin.ModelAdmin):
    list_display = ['product', 'interaction_type', 'user', 'session_key', 'ip_address', 'created_at']
    list_filter = ['interaction_type', 'created_at', 'product__category']
    search_fields = ['product__name', 'user__email', 'session_key', 'ip_address']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'created_at'


@admin.register(DailyProductStats)
class DailyProductStatsAdmin(admin.ModelAdmin):
    list_display = ['product', 'date', 'views', 'clicks', 'add_to_cart', 'purchases', 'revenue']
    list_filter = ['date', 'product__category']
    search_fields = ['product__name']
    date_hierarchy = 'date'


@admin.register(DailyCategoryStats)
class DailyCategoryStatsAdmin(admin.ModelAdmin):
    list_display = ['category', 'date', 'views', 'clicks', 'add_to_cart', 'purchases', 'revenue']
    list_filter = ['date']
    search_fields = ['category__name']
    date_hierarchy = 'date'


@admin.register(UserBehaviorSummary)
class UserBehaviorSummaryAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'session_key', 'viewed', 'added_to_cart', 'purchased', 'view_count']
    list_filter = ['viewed', 'added_to_cart', 'purchased', 'removed_from_cart']
    search_fields = ['product__name', 'user__email', 'session_key']
