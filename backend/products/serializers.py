from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for product categories."""
    
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'is_active', 'product_count']
    
    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product images."""
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order']


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for product list view."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description', 'price', 'discount_price',
            'final_price', 'discount_percentage', 'category', 'category_name',
            'image', 'stock', 'in_stock', 'brand', 'is_featured'
        ]
    
    def get_image(self, obj):
        # Prefer image_url over uploaded image
        if obj.image_url:
            return obj.image_url
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for product detail view."""
    
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'price', 'discount_price', 'final_price', 'discount_percentage',
            'category', 'image', 'images', 'stock', 'in_stock', 'sku',
            'brand', 'specifications', 'is_featured', 'created_at'
        ]
    
    def get_image(self, obj):
        # Prefer image_url over uploaded image
        if obj.image_url:
            return obj.image_url
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating products (admin only)."""
    
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 'short_description', 'price',
            'discount_price', 'category', 'image', 'image_url', 'stock', 'sku', 'brand',
            'specifications', 'is_active', 'is_featured'
        ]
        extra_kwargs = {
            'slug': {'required': False},
            'image': {'required': False},
            'image_url': {'required': False},
        }
