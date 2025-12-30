from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import (
    CategorySerializer, ProductListSerializer,
    ProductDetailSerializer, ProductCreateUpdateSerializer
)


class CategoryListView(generics.ListAPIView):
    """List all active categories."""
    
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    """List all active products with filtering and search."""
    
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'brand', 'is_featured']
    search_fields = ['name', 'description', 'brand', 'sku']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']


class ProductDetailView(generics.RetrieveAPIView):
    """Get product detail."""
    
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class FeaturedProductsView(generics.ListAPIView):
    """List featured products."""
    
    queryset = Product.objects.filter(is_active=True, is_featured=True).select_related('category')[:8]
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class ProductsByCategoryView(generics.ListAPIView):
    """List products by category slug."""
    
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'brand']
    ordering_fields = ['price', 'created_at', 'name']
    
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        return Product.objects.filter(
            is_active=True,
            category__slug=category_slug
        ).select_related('category')


# Admin Views
class AdminProductListCreateView(generics.ListCreateAPIView):
    """Admin: List and create products."""
    
    queryset = Product.objects.all().select_related('category')
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_active', 'is_featured']
    search_fields = ['name', 'sku']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductListSerializer


class AdminProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Get, update, delete product."""
    
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminCategoryListCreateView(generics.ListCreateAPIView):
    """Admin: List and create categories."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class AdminCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Get, update, delete category."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
