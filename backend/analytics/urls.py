from django.urls import path
from .views import (
    TrackInteractionView,
    DashboardOverviewView,
    MostViewedProductsView,
    MostAddedToCartProductsView,
    MostPurchasedProductsView,
    ViewedButNotPurchasedView,
    AddedToCartButRemovedView,
    TimeSeriesAnalyticsView,
    CategoryAnalyticsView,
    FunnelAnalyticsView,
    InteractionHistoryView,
    ExportAnalyticsView,
    ExportPDFView,
)

urlpatterns = [
    # Public tracking endpoint
    path('track/', TrackInteractionView.as_view(), name='track-interaction'),
    
    # Admin analytics endpoints
    path('dashboard/', DashboardOverviewView.as_view(), name='dashboard-overview'),
    path('most-viewed/', MostViewedProductsView.as_view(), name='most-viewed'),
    path('most-added-to-cart/', MostAddedToCartProductsView.as_view(), name='most-added-to-cart'),
    path('most-purchased/', MostPurchasedProductsView.as_view(), name='most-purchased'),
    path('viewed-not-purchased/', ViewedButNotPurchasedView.as_view(), name='viewed-not-purchased'),
    path('cart-abandoned/', AddedToCartButRemovedView.as_view(), name='cart-abandoned'),
    path('time-series/', TimeSeriesAnalyticsView.as_view(), name='time-series'),
    path('categories/', CategoryAnalyticsView.as_view(), name='category-analytics'),
    path('funnel/', FunnelAnalyticsView.as_view(), name='funnel-analytics'),
    path('history/', InteractionHistoryView.as_view(), name='interaction-history'),
    path('export/csv/', ExportAnalyticsView.as_view(), name='export-csv'),
    path('export/pdf/', ExportPDFView.as_view(), name='export-pdf'),
]
