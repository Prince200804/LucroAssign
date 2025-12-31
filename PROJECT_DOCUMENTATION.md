# 📚 LucroAssign - Complete Project Documentation

## E-Commerce Analytics Platform with Django REST Framework & Vue.js

**Author:** Prince200804  
**Tech Stack:** Django 5.x + Vue.js 3 + Vuetify 3 + Stripe Payment  
**GitHub:** https://github.com/Prince200804/LucroAssign

---

# Table of Contents

1. [Project Architecture Overview](#1-project-architecture-overview)
2. [Backend - Django REST Framework](#2-backend---django-rest-framework)
   - [Core Settings](#21-core-settings-backendsettingspy)
   - [URL Configuration](#22-url-configuration-backendcoreurlspy)
   - [Users App](#23-users-app)
   - [Products App](#24-products-app)
   - [Cart App](#25-cart-app)
   - [Orders App](#26-orders-app)
   - [Analytics App](#27-analytics-app)
3. [Frontend - Vue.js 3](#3-frontend---vuejs-3)
   - [API Service](#31-api-service)
   - [Pinia Stores](#32-pinia-stores)
   - [Vue Router](#33-vue-router)
4. [Database Design](#4-database-design)
5. [API Endpoints Reference](#5-api-endpoints-reference)
6. [Interview Questions & Answers](#6-interview-questions--answers)

---

# 1. Project Architecture Overview

## 1.1 Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Backend | Django 5.x | Python web framework |
| API | Django REST Framework | RESTful API creation |
| Auth | JWT (SimpleJWT) | Token-based authentication |
| Database | SQLite/PostgreSQL | Data storage |
| Frontend | Vue.js 3 | Reactive UI framework |
| UI Library | Vuetify 3 | Material Design components |
| State | Pinia | State management |
| Payment | Stripe | Payment processing |

## 1.2 Project Structure

```
LucroAssign/
├── backend/                 # Django Backend
│   ├── core/               # Main Django project
│   │   ├── settings.py     # Configuration
│   │   ├── urls.py         # Main URL routing
│   │   └── wsgi.py         # WSGI entry point
│   ├── users/              # User authentication
│   ├── products/           # Product catalog
│   ├── cart/               # Shopping cart
│   ├── orders/             # Order processing
│   └── analytics/          # User behavior tracking
├── frontend/               # Vue.js Frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── views/          # Page components
│   │   ├── stores/         # Pinia state stores
│   │   ├── router/         # Vue Router config
│   │   └── services/       # API services
│   └── package.json
└── README.md
```

---

# 2. Backend - Django REST Framework

## 2.1 Core Settings (`backend/core/settings.py`)

```python
"""
Django settings for E-Commerce Analytics Platform.
"""

from pathlib import Path
from datetime import timedelta
import os

# BASE_DIR: Root directory of the project
# Path(__file__) = current file (settings.py)
# .resolve() = get absolute path
# .parent.parent = go up two directories (core -> backend)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY: Used for cryptographic signing
# In production, this should NEVER be hardcoded
# os.environ.get() tries to get from environment variables first
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-key-for-development')

# DEBUG: Shows detailed error pages
# NEVER set True in production (security risk)
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

# ALLOWED_HOSTS: Domains that can access this Django app
# Prevents HTTP Host header attacks
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
ALLOWED_HOSTS += ['.railway.app', '.vercel.app']  # Production hosts

# INSTALLED_APPS: All Django apps to load
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',        # Admin panel
    'django.contrib.auth',         # Authentication framework
    'django.contrib.contenttypes', # Content type framework
    'django.contrib.sessions',     # Session framework
    'django.contrib.messages',     # Messaging framework
    'django.contrib.staticfiles',  # Static file serving
    
    # Third-party apps
    'rest_framework',              # Django REST Framework
    'rest_framework_simplejwt',    # JWT authentication
    'corsheaders',                 # CORS handling
    'django_filters',              # Filtering for DRF
    
    # Local apps (our custom apps)
    'users',      # User management
    'products',   # Product catalog
    'cart',       # Shopping cart
    'orders',     # Order processing
    'analytics',  # Analytics tracking
]

# MIDDLEWARE: Request/Response processing pipeline
# Order matters! Requests go top-to-bottom, responses bottom-to-top
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',      # Security checks
    'whitenoise.middleware.WhiteNoiseMiddleware',         # Static file serving
    'corsheaders.middleware.CorsMiddleware',              # CORS headers (MUST be before CommonMiddleware)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'analytics.middleware.InteractionTrackingMiddleware', # Custom: track user behavior
]

# REST Framework Configuration
REST_FRAMEWORK = {
    # How to authenticate API requests
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT tokens
        'rest_framework.authentication.SessionAuthentication',        # Session cookies
    ],
    # Default permissions (AllowAny = no auth required by default)
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    # Filtering backends
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',  # Field filtering
        'rest_framework.filters.SearchFilter',                # Text search
        'rest_framework.filters.OrderingFilter',              # Result ordering
    ],
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,  # 12 items per page
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),   # Token valid for 1 day
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh valid for 7 days
    'ROTATE_REFRESH_TOKENS': True,                # Issue new refresh on use
    'BLACKLIST_AFTER_ROTATION': True,             # Invalidate old refresh tokens
}

# CORS Settings - Allow frontend to access API
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',                    # Vite dev server
    'https://lucro-assign.vercel.app',         # Production frontend
]
CORS_ALLOW_CREDENTIALS = True  # Allow cookies/auth headers

# Custom User Model
AUTH_USER_MODEL = 'users.User'  # Use our custom User model
```

### Key Concepts Explained:

1. **BASE_DIR**: The root directory of the project, used to construct file paths
2. **SECRET_KEY**: Cryptographic key for sessions, password reset tokens, etc.
3. **MIDDLEWARE**: Like filters that process every request/response
4. **REST_FRAMEWORK**: Configuration for Django REST Framework
5. **CORS**: Cross-Origin Resource Sharing - allows frontend on different domain to access API

---

## 2.2 URL Configuration (`backend/core/urls.py`)

```python
"""
URL configuration for E-Commerce Analytics Platform.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Health check endpoint for deployment monitoring
def health_check(request):
    """Railway/Render check this endpoint to verify app is running"""
    return JsonResponse({'status': 'healthy', 'message': 'API is running'})

urlpatterns = [
    # Admin panel - Django's built-in admin interface
    path('admin/', admin.site.urls),
    
    # Health check for deployment platforms
    path('api/health/', health_check, name='health_check'),
    
    # Include URLs from each app
    # include() delegates URL handling to the app's urls.py
    path('api/users/', include('users.urls')),       # /api/users/...
    path('api/products/', include('products.urls')), # /api/products/...
    path('api/cart/', include('cart.urls')),         # /api/cart/...
    path('api/orders/', include('orders.urls')),     # /api/orders/...
    path('api/analytics/', include('analytics.urls')), # /api/analytics/...
]
```

### URL Pattern Explanation:
- `path('prefix/', include('app.urls'))` - Delegates all URLs starting with 'prefix/' to that app
- Example: `/api/users/login/` → handled by `users/urls.py`

---

## 2.3 Users App

### 2.3.1 Models (`backend/users/models.py`)

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    AbstractUser provides: username, email, password, first_name, last_name, etc.
    We add additional fields specific to our e-commerce platform.
    """
    
    # UUID primary key instead of auto-increment integer
    # Benefits: Can't guess user IDs, better for distributed systems
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Make email unique and required
    email = models.EmailField(unique=True)
    
    # Additional profile fields
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, default='India')
    
    # Admin flag for our app (separate from Django's is_staff)
    is_admin = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # Set once on creation
    updated_at = models.DateTimeField(auto_now=True)       # Updated on every save
    
    # Use email instead of username for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Required when creating superuser
    
    class Meta:
        db_table = 'users'  # Custom table name in database
    
    def __str__(self):
        return self.email
```

### Key Model Concepts:

1. **AbstractUser**: Django's built-in user model that we extend
2. **UUIDField**: Universally Unique Identifier - more secure than integers
3. **auto_now_add**: Automatically set to current time when object is created
4. **auto_now**: Automatically update to current time on every save
5. **USERNAME_FIELD**: Which field to use for login (we use email)

### 2.3.2 Views (`backend/users/views.py`)

```python
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    
    CreateAPIView: DRF generic view that handles POST requests to create objects.
    It automatically:
    1. Validates data using serializer
    2. Creates the object
    3. Returns appropriate response
    """
    
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can register
    
    def create(self, request, *args, **kwargs):
        # Validate and create user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Raises 400 if invalid
        user = serializer.save()
        
        # Generate JWT tokens for immediate login after registration
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    API endpoint for user login.
    
    APIView: Base class for all views. We use it when we need full control
    over request handling (not using generic views).
    """
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # authenticate() checks credentials against database
        # Returns User object if valid, None if invalid
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
```

### View Concepts:

1. **generics.CreateAPIView**: Pre-built view for creating objects (handles POST)
2. **APIView**: Base view class for custom logic
3. **permission_classes**: Who can access this endpoint
4. **serializer.is_valid(raise_exception=True)**: Validate data, raise 400 error if invalid

---

## 2.4 Products App

### 2.4.1 Models (`backend/products/models.py`)

```python
from django.db import models
import uuid

class Category(models.Model):
    """Product category for organizing products."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)  # URL-friendly name
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'categories'
        ordering = ['name']  # Default ordering when querying
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model for e-commerce."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # ForeignKey creates a many-to-one relationship
    # on_delete=CASCADE: Delete products when category is deleted
    # related_name: Access products from category (category.products.all())
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    
    image_url = models.URLField(max_length=500, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True)  # Stock Keeping Unit
    brand = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'products'
        ordering = ['-created_at']  # Newest first
    
    @property
    def final_price(self):
        """
        @property decorator makes this method accessible like an attribute.
        Usage: product.final_price (not product.final_price())
        """
        return self.discount_price if self.discount_price else self.price
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage."""
        if self.discount_price and self.price > 0:
            return round((1 - self.discount_price / self.price) * 100)
        return 0
    
    @property
    def in_stock(self):
        """Check if product is in stock."""
        return self.stock > 0
```

### Model Relationships:

1. **ForeignKey**: Many-to-one relationship (many products belong to one category)
2. **related_name**: Reverse accessor (category.products.all())
3. **@property**: Computed field that acts like an attribute

### 2.4.2 Views (`backend/products/views.py`)

```python
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

class ProductListView(generics.ListAPIView):
    """
    List all active products with filtering, search, and ordering.
    
    ListAPIView: Generic view for listing objects (handles GET requests)
    """
    
    # QuerySet: Products that are active, with category pre-loaded
    # select_related: SQL JOIN to fetch category in same query (optimization)
    queryset = Product.objects.filter(is_active=True).select_related('category')
    
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    
    # Enable filtering, search, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Exact match filtering on these fields
    # Usage: /api/products/?category=<uuid>&brand=Nike
    filterset_fields = ['category', 'brand', 'is_featured']
    
    # Text search on these fields
    # Usage: /api/products/?search=laptop
    search_fields = ['name', 'description', 'brand', 'sku']
    
    # Allow ordering by these fields
    # Usage: /api/products/?ordering=-price (descending)
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']  # Default ordering


class ProductDetailView(generics.RetrieveAPIView):
    """
    Get single product detail.
    
    RetrieveAPIView: Generic view for retrieving single object (GET /products/<slug>/)
    """
    
    # prefetch_related: For many-to-many or reverse FK (optimization)
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'  # Use slug instead of id in URL
```

### QuerySet Optimization:

1. **select_related**: One-to-many/FK - Single query with JOIN
2. **prefetch_related**: Many-to-many - Separate query, then Python joins

---

## 2.5 Cart App

### 2.5.1 Models (`backend/cart/models.py`)

```python
from django.db import models
from django.conf import settings
from products.models import Product
import uuid

class Cart(models.Model):
    """
    Shopping cart model.
    Supports both authenticated users and anonymous sessions.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # For logged-in users
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # References custom User model
        on_delete=models.CASCADE,
        related_name='carts',
        null=True,
        blank=True
    )
    
    # For anonymous users (tracked by session)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    
    @property
    def total_items(self):
        """Sum of quantities of all items in cart."""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def subtotal(self):
        """Sum of total_price for all items."""
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """Individual item in cart."""
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ['cart', 'product']  # One entry per product per cart
    
    @property
    def unit_price(self):
        return self.product.final_price
    
    @property
    def total_price(self):
        return self.unit_price * self.quantity
```

### 2.5.2 Views (`backend/cart/views.py`)

```python
class CartMixin:
    """
    Mixin: Reusable piece of code that can be added to multiple views.
    This mixin provides cart retrieval logic.
    """
    
    def get_cart(self, request):
        """Get or create cart based on user authentication status."""
        if request.user.is_authenticated:
            # Logged-in user: get or create cart linked to user
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            # Anonymous user: use session key
            session_key = request.session.session_key
            if not session_key:
                request.session.create()  # Create new session
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart


class AddToCartView(CartMixin, APIView):
    """Add item to cart."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # get_object_or_404: Returns object or raises 404 error
        product = get_object_or_404(
            Product, 
            id=serializer.validated_data['product_id'], 
            is_active=True
        )
        
        quantity = serializer.validated_data['quantity']
        
        # Check stock availability
        if product.stock < quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart = self.get_cart(request)
        
        # get_or_create: Get existing or create new
        # Returns tuple: (object, was_created_boolean)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Item already existed, increase quantity
            cart_item.quantity += quantity
            cart_item.save()
        
        # Track for analytics
        track_interaction(
            request=request,
            product=product,
            interaction_type='add_to_cart',
            metadata={'quantity': quantity}
        )
        
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
```

---

## 2.6 Orders App

### 2.6.1 Models (`backend/orders/models.py`)

```python
class Order(models.Model):
    """Order model with full order lifecycle tracking."""
    
    # Status choices as list of tuples
    # First element: database value, Second: human-readable name
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    
    # Order can belong to a user or be anonymous
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # Keep order even if user is deleted
        null=True,
        blank=True
    )
    
    # Shipping details
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    shipping_address = models.TextField()
    
    # Order totals
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Stripe integration
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        """Override save to auto-generate order number."""
        if not self.order_number:
            import random
            import string
            self.order_number = 'ORD' + ''.join(random.choices(string.digits, k=10))
        super().save(*args, **kwargs)
```

### 2.6.2 Stripe Payment Integration (`backend/orders/views.py`)

```python
import stripe

# Configure Stripe with API key from settings
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripePaymentIntentView(APIView):
    """
    Create Stripe PaymentIntent for checkout.
    
    PaymentIntent: Stripe object that tracks payment lifecycle.
    """
    
    def post(self, request):
        cart = self.get_cart(request)
        
        if not cart or cart.items.count() == 0:
            return Response({'error': 'Cart is empty'}, status=400)
        
        # Convert to paise (smallest currency unit)
        # Stripe requires amount in smallest unit (100 = ₹1)
        amount_in_paise = int(float(cart.total) * 100)
        
        try:
            # Create PaymentIntent via Stripe API
            intent = stripe.PaymentIntent.create(
                amount=amount_in_paise,
                currency='inr',
                automatic_payment_methods={'enabled': True},
                metadata={'cart_id': str(cart.id)}
            )
            
            return Response({
                'client_secret': intent.client_secret,  # Frontend needs this
                'payment_intent_id': intent.id,
                'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            })
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=500)
```

---

## 2.7 Analytics App

### 2.7.1 Models (`backend/analytics/models.py`)

```python
class ProductInteraction(models.Model):
    """
    Track all product interactions for analytics.
    
    This model stores every user action for analysis:
    - Page views
    - Add to cart
    - Purchases
    - etc.
    """
    
    INTERACTION_TYPES = [
        ('view', 'Product View'),
        ('click', 'Product Click'),
        ('add_to_cart', 'Added to Cart'),
        ('remove_from_cart', 'Removed from Cart'),
        ('purchase', 'Purchased'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    metadata = models.JSONField(default=dict)  # Store additional data as JSON
    ip_address = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Database indexes for faster queries
        indexes = [
            models.Index(fields=['product', 'interaction_type']),
            models.Index(fields=['created_at']),
        ]
```

### 2.7.2 Analytics Dashboard View (`backend/analytics/views.py`)

```python
class DashboardOverviewView(APIView):
    """Get dashboard overview statistics."""
    
    permission_classes = [IsAdminOrStaff]  # Only admins can access
    
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # Filter interactions within date range
        interactions = ProductInteraction.objects.filter(created_at__gte=start_date)
        
        # Aggregate statistics using Django ORM
        total_views = interactions.filter(interaction_type='view').count()
        total_add_to_cart = interactions.filter(interaction_type='add_to_cart').count()
        total_purchases = interactions.filter(interaction_type='purchase').count()
        
        # Calculate conversion rates
        view_to_cart_rate = (total_add_to_cart / total_views * 100) if total_views > 0 else 0
        overall_conversion = (total_purchases / total_views * 100) if total_views > 0 else 0
        
        return Response({
            'period_days': days,
            'total_views': total_views,
            'total_add_to_cart': total_add_to_cart,
            'total_purchases': total_purchases,
            'conversion_rates': {
                'view_to_cart': round(view_to_cart_rate, 2),
                'overall': round(overall_conversion, 2),
            },
        })
```

---

# 3. Frontend - Vue.js 3

## 3.1 API Service (`frontend/src/services/api.js`)

```javascript
import axios from 'axios'

// Get API URL from environment variable
// import.meta.env is Vite's way to access environment variables
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000, // 15 second timeout
})

// REQUEST INTERCEPTOR
// Runs before every request is sent
api.interceptors.request.use(
  (config) => {
    // Add JWT token to Authorization header
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// RESPONSE INTERCEPTOR
// Runs after every response is received
api.interceptors.response.use(
  (response) => response,  // Success: return response as-is
  async (error) => {
    const originalRequest = error.config

    // If 401 Unauthorized and haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // Try to refresh the token
        const refreshToken = localStorage.getItem('refresh_token')
        const response = await axios.post(`${API_BASE_URL}/users/token/refresh/`, {
          refresh: refreshToken,
        })

        // Store new access token
        const { access } = response.data
        localStorage.setItem('access_token', access)

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access}`
        return api(originalRequest)
      } catch (refreshError) {
        // Refresh failed, clear tokens (user needs to login again)
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      }
    }

    return Promise.reject(error)
  }
)

export default api
```

### Key Concepts:

1. **axios.create()**: Creates a configured axios instance
2. **Interceptors**: Functions that run before/after every request
3. **Token Refresh**: Automatically refresh expired tokens

---

## 3.2 Pinia Stores

### 3.2.1 Auth Store (`frontend/src/stores/auth.js`)

```javascript
import { defineStore } from 'pinia'
import api from '@/services/api'

// defineStore creates a reactive store
// First argument: unique store ID
// Second argument: store definition
export const useAuthStore = defineStore('auth', {
  // STATE: Reactive data
  state: () => ({
    user: null,      // Current user object
    isAdmin: false,  // Admin flag
    initialized: false,
  }),

  // GETTERS: Computed properties
  getters: {
    isAuthenticated: (state) => !!state.user,  // True if user exists
  },

  // ACTIONS: Methods to modify state
  actions: {
    async login(email, password) {
      try {
        const response = await api.post('/users/login/', { email, password })
        const { user, tokens } = response.data

        // Store tokens in localStorage
        localStorage.setItem('access_token', tokens.access)
        localStorage.setItem('refresh_token', tokens.refresh)

        // Update state
        this.user = user
        await this.checkAdmin()

        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.error || 'Login failed' 
        }
      }
    },

    async logout() {
      // Clear tokens
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      
      // Reset state
      this.user = null
      this.isAdmin = false
    },

    async fetchUser() {
      // Get current user profile
      const response = await api.get('/users/profile/')
      this.user = response.data
    },
  },
})
```

### 3.2.2 Cart Store (`frontend/src/stores/cart.js`)

```javascript
export const useCartStore = defineStore('cart', {
  state: () => ({
    cart: null,
    loading: false,
  }),

  getters: {
    items: (state) => state.cart?.items || [],
    totalItems: (state) => state.cart?.total_items || 0,
    total: (state) => state.cart?.total || 0,
  },

  actions: {
    async addToCart(productId, quantity = 1) {
      try {
        this.loading = true
        const response = await api.post('/cart/add/', {
          product_id: productId,
          quantity,
        })
        this.cart = response.data  // Update cart with response
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.error || 'Failed to add to cart' 
        }
      } finally {
        this.loading = false  // Always runs (success or error)
      }
    },
  },
})
```

---

## 3.3 Vue Router (`frontend/src/router/index.js`)

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    // Lazy loading: Component loaded only when route is visited
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/products/:slug',  // Dynamic route parameter
    name: 'ProductDetail',
    component: () => import('@/views/ProductDetailView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { guest: true }  // Only for non-authenticated users
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { requiresAuth: true }  // Requires authentication
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('@/views/admin/DashboardView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }  // Admin only
  },
]

const router = createRouter({
  history: createWebHistory(),  // HTML5 History mode (clean URLs)
  routes,
})

// NAVIGATION GUARD
// Runs before every navigation
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Initialize auth state if not done
  if (!authStore.initialized) {
    await authStore.initializeAuth()
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')  // Redirect to login
    return
  }

  // Check if route requires admin
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/')  // Redirect to home
    return
  }

  // Check if route is for guests only
  if (to.meta.guest && authStore.isAuthenticated) {
    next('/')  // Already logged in, go to home
    return
  }

  next()  // Allow navigation
})

export default router
```

---

# 4. Database Design

## Entity Relationship Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    User     │     │   Category  │     │   Product   │
├─────────────┤     ├─────────────┤     ├─────────────┤
│ id (UUID)   │     │ id (UUID)   │     │ id (UUID)   │
│ email       │     │ name        │     │ name        │
│ username    │     │ slug        │     │ slug        │
│ password    │     │ description │     │ price       │
│ first_name  │     │ is_active   │     │ category_id │──┐
│ last_name   │     └─────────────┘     │ stock       │  │
│ is_admin    │                         │ is_active   │  │
└─────────────┘                         └─────────────┘  │
       │                                       │         │
       │                                       │         │
       ▼                                       ▼         │
┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│    Cart     │     │  CartItem   │     │ (FK)        │◄─┘
├─────────────┤     ├─────────────┤     └─────────────┘
│ id (UUID)   │◄────│ cart_id     │
│ user_id     │     │ product_id  │────►┌─────────────┐
│ session_key │     │ quantity    │     │   Product   │
└─────────────┘     └─────────────┘     └─────────────┘
       │
       │
       ▼
┌─────────────┐     ┌─────────────┐
│   Order     │     │  OrderItem  │
├─────────────┤     ├─────────────┤
│ id (UUID)   │◄────│ order_id    │
│ user_id     │     │ product_id  │
│ order_number│     │ quantity    │
│ status      │     │ unit_price  │
│ total       │     └─────────────┘
└─────────────┘
```

---

# 5. API Endpoints Reference

## Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/register/` | Register new user |
| POST | `/api/users/login/` | Login user |
| POST | `/api/users/logout/` | Logout user |
| GET | `/api/users/profile/` | Get user profile |
| PATCH | `/api/users/profile/` | Update profile |

## Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products |
| GET | `/api/products/<slug>/` | Get product detail |
| GET | `/api/products/categories/` | List categories |
| GET | `/api/products/featured/` | Featured products |

## Cart
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cart/` | Get cart |
| POST | `/api/cart/add/` | Add to cart |
| PATCH | `/api/cart/update/<id>/` | Update quantity |
| DELETE | `/api/cart/remove/<id>/` | Remove item |

## Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/orders/create-payment-intent/` | Create Stripe payment |
| POST | `/api/orders/create/` | Create order |
| GET | `/api/orders/` | List user orders |
| GET | `/api/orders/<id>/` | Order detail |

## Analytics (Admin)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/dashboard/` | Dashboard stats |
| GET | `/api/analytics/most-viewed/` | Most viewed products |
| GET | `/api/analytics/most-purchased/` | Best sellers |

---

# 6. Interview Questions & Answers

## Django Questions

### Q1: What is Django REST Framework and why use it?
**Answer:** Django REST Framework (DRF) is a toolkit for building Web APIs in Django. Key features:
- **Serializers**: Convert complex data types (models) to JSON and vice versa
- **Generic Views**: Pre-built views for common operations (CRUD)
- **Authentication**: Built-in support for JWT, Token, Session auth
- **Permissions**: Fine-grained access control
- **Filtering/Pagination**: Easy data filtering and pagination

### Q2: Explain the difference between `select_related` and `prefetch_related`
**Answer:**
- **select_related**: Uses SQL JOIN for ForeignKey/OneToOne relationships. Single query.
  ```python
  Product.objects.select_related('category')  # One query with JOIN
  ```
- **prefetch_related**: Separate queries for ManyToMany/reverse FK. Better for multiple related objects.
  ```python
  Category.objects.prefetch_related('products')  # Two queries, joined in Python
  ```

### Q3: What is a Django Serializer?
**Answer:** Serializers convert complex data types (Django models) to Python native types that can be rendered to JSON. They also handle deserialization (JSON → model) and validation.
```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
```

### Q4: Explain Django Middleware
**Answer:** Middleware is a framework of hooks into Django's request/response processing. Each middleware component processes:
1. **Request**: Before view is called (top to bottom)
2. **Response**: After view returns (bottom to top)

Common uses: Authentication, CORS, logging, request modification.

### Q5: What is JWT authentication?
**Answer:** JSON Web Token (JWT) is a stateless authentication method:
1. User logs in with credentials
2. Server returns two tokens: Access (short-lived) and Refresh (long-lived)
3. Client sends Access token in `Authorization: Bearer <token>` header
4. When Access expires, use Refresh token to get new Access token

Advantages: Stateless (no server-side session storage), scalable, can contain user data (claims).

---

## Vue.js Questions

### Q6: What is Pinia and how does it differ from Vuex?
**Answer:** Pinia is the official state management library for Vue 3. Differences from Vuex:
- **No mutations**: Actions directly modify state
- **TypeScript support**: Better out-of-the-box
- **Simpler API**: Less boilerplate
- **Devtools support**: Full Vue devtools integration

### Q7: Explain Vue Router navigation guards
**Answer:** Navigation guards are hooks that run during navigation:
- **beforeEach**: Before every navigation (global)
- **beforeEnter**: Before entering specific route
- **beforeRouteLeave**: Before leaving component

Used for: Authentication checks, data fetching, preventing unauthorized access.

### Q8: What are Vue Composables?
**Answer:** Composables are functions that leverage Vue's Composition API to encapsulate reusable logic:
```javascript
function useCounter() {
  const count = ref(0)
  const increment = () => count.value++
  return { count, increment }
}
```

### Q9: Explain Vue's reactivity system
**Answer:** Vue uses a Proxy-based reactivity system:
1. `ref()`: For primitive values, wrapped in `.value`
2. `reactive()`: For objects, deeply reactive
3. `computed()`: Cached computed values
4. Vue tracks dependencies and updates DOM when reactive data changes

---

## General Questions

### Q10: Explain the request flow in this project
**Answer:**
1. **Frontend**: User action triggers API call via axios
2. **Request**: Goes to Django URL router
3. **Middleware**: CORS, Auth, etc. process request
4. **View**: DRF view processes request
5. **Serializer**: Validates input, serializes output
6. **Model**: Database operations
7. **Response**: JSON returned to frontend
8. **Store**: Pinia store updates state
9. **Component**: Vue re-renders with new data

### Q11: How does payment processing work with Stripe?
**Answer:**
1. Frontend requests Payment Intent from backend
2. Backend creates PaymentIntent via Stripe API, returns client_secret
3. Frontend uses Stripe.js to collect card details securely
4. Frontend confirms payment with client_secret
5. Stripe processes payment
6. Frontend sends payment_intent_id to backend
7. Backend verifies payment with Stripe API
8. If successful, create order

### Q12: How do you handle authentication in this project?
**Answer:**
1. **Registration/Login**: Server returns JWT tokens
2. **Storage**: Tokens stored in localStorage
3. **API Calls**: Axios interceptor adds token to Authorization header
4. **Token Refresh**: When 401 received, try to refresh token
5. **Logout**: Clear tokens from storage

### Q13: Explain the analytics tracking system
**Answer:**
1. **ProductInteraction model**: Stores all user actions
2. **track_interaction() utility**: Helper to create interaction records
3. **Middleware**: Can track page views automatically
4. **Frontend tracking**: API calls on user actions (add to cart, etc.)
5. **Admin Dashboard**: Aggregates data for visualization

---

## Deployment Questions

### Q14: How is CORS configured in this project?
**Answer:**
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'https://lucro-assign.vercel.app',
]
CORS_ALLOW_CREDENTIALS = True
```
- `django-cors-headers` middleware handles CORS
- Origins must match exactly (no trailing slash)
- Credentials allow cookies/auth headers across origins

### Q15: Explain the deployment architecture
**Answer:**
- **Frontend (Vercel)**: Static Vue.js build served via CDN
- **Backend (Railway)**: Django app with Gunicorn WSGI server
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Static Files**: WhiteNoise serves Django static files

Environment variables configure each environment separately.

---

## Code Quality Questions

### Q16: What design patterns are used in this project?
**Answer:**
1. **MVC/MTV**: Django's Model-Template-View pattern
2. **Repository Pattern**: Models abstract database access
3. **Singleton**: Pinia stores are singletons
4. **Observer**: Vue's reactivity system
5. **Factory**: Serializers create/validate objects
6. **Mixin**: CartMixin for shared cart logic

### Q17: How is code organized in the backend?
**Answer:** Django apps separation:
- **users**: Authentication, profiles
- **products**: Catalog management
- **cart**: Shopping cart logic
- **orders**: Order processing, payment
- **analytics**: User behavior tracking

Each app has: models.py, views.py, serializers.py, urls.py

---

# Quick Reference Card

## Django Commands
```bash
python manage.py runserver          # Start development server
python manage.py makemigrations     # Create migration files
python manage.py migrate            # Apply migrations
python manage.py createsuperuser    # Create admin user
python manage.py shell              # Django shell
python manage.py seed_data          # Seed sample data
```

## Vue Commands
```bash
npm install                # Install dependencies
npm run dev               # Start dev server
npm run build             # Build for production
```

## Git Commands
```bash
git add .                 # Stage all changes
git commit -m "message"   # Commit
git push                  # Push to remote
```

---

**End of Documentation**

*This document covers the complete LucroAssign E-Commerce Analytics Platform codebase with line-by-line explanations, database design, API reference, and interview preparation questions.*
