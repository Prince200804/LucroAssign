from django.urls import path
from .views import (
    CreateOrderView, OrderListView, OrderDetailView, TrackOrderView,
    CreateStripePaymentIntentView, AdminOrderListView, AdminOrderDetailView,
    AdminUpdateOrderStatusView, AdminOrderStatsView,
    ExportOrdersExcelView, ExportOrdersPDFView,
    ExportAnalyticsExcelView, ExportAnalyticsPDFView,
    ExportProductsExcelView
)

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('stripe/create-payment-intent/', CreateStripePaymentIntentView.as_view(), name='create-stripe-payment-intent'),
    path('track/<str:order_number>/', TrackOrderView.as_view(), name='track-order'),
    path('<uuid:pk>/', OrderDetailView.as_view(), name='order-detail'),
    
    # Admin endpoints
    path('admin/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/stats/', AdminOrderStatsView.as_view(), name='admin-order-stats'),
    path('admin/<uuid:pk>/', AdminOrderDetailView.as_view(), name='admin-order-detail'),
    path('admin/<uuid:pk>/update-status/', AdminUpdateOrderStatusView.as_view(), name='admin-update-order-status'),
    
    # Export endpoints
    path('admin/export/orders/excel/', ExportOrdersExcelView.as_view(), name='export-orders-excel'),
    path('admin/export/orders/pdf/', ExportOrdersPDFView.as_view(), name='export-orders-pdf'),
    path('admin/export/analytics/excel/', ExportAnalyticsExcelView.as_view(), name='export-analytics-excel'),
    path('admin/export/analytics/pdf/', ExportAnalyticsPDFView.as_view(), name='export-analytics-pdf'),
    path('admin/export/products/excel/', ExportProductsExcelView.as_view(), name='export-products-excel'),
]
