from django.urls import path
from .views import (
    CategoryListView, ProductListView, ProductDetailView,
    FeaturedProductsView, ProductsByCategoryView,
    AdminProductListCreateView, AdminProductDetailView,
    AdminCategoryListCreateView, AdminCategoryDetailView
)

urlpatterns = [
    # Public endpoints
    path('', ProductListView.as_view(), name='product-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('featured/', FeaturedProductsView.as_view(), name='featured-products'),
    path('category/<slug:category_slug>/', ProductsByCategoryView.as_view(), name='products-by-category'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    
    # Admin endpoints
    path('admin/products/', AdminProductListCreateView.as_view(), name='admin-product-list'),
    path('admin/products/<uuid:pk>/', AdminProductDetailView.as_view(), name='admin-product-detail'),
    path('admin/categories/', AdminCategoryListCreateView.as_view(), name='admin-category-list'),
    path('admin/categories/<uuid:pk>/', AdminCategoryDetailView.as_view(), name='admin-category-detail'),
]
