from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, AddToCartSerializer, UpdateCartItemSerializer
from products.models import Product
from analytics.utils import track_interaction


class CartMixin:
    """Mixin to get or create cart for user or session."""
    
    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart


class CartView(CartMixin, APIView):
    """Get current cart."""
    
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(CartMixin, APIView):
    """Add item to cart."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = get_object_or_404(Product, id=serializer.validated_data['product_id'], is_active=True)
        quantity = serializer.validated_data['quantity']
        
        if product.stock < quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart = self.get_cart(request)
        
        # Check if item already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                return Response(
                    {'error': 'Insufficient stock'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.save()
        
        # Track interaction
        track_interaction(
            request=request,
            product=product,
            interaction_type='add_to_cart',
            metadata={'quantity': quantity}
        )
        
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class UpdateCartItemView(CartMixin, APIView):
    """Update cart item quantity."""
    
    permission_classes = [permissions.AllowAny]
    
    def patch(self, request, item_id):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        quantity = serializer.validated_data['quantity']
        
        if cart_item.product.stock < quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response(CartSerializer(cart).data)


class RemoveFromCartView(CartMixin, APIView):
    """Remove item from cart."""
    
    permission_classes = [permissions.AllowAny]
    
    def delete(self, request, item_id):
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        product = cart_item.product
        
        # Track interaction
        track_interaction(
            request=request,
            product=product,
            interaction_type='remove_from_cart',
            metadata={'quantity': cart_item.quantity}
        )
        
        cart_item.delete()
        
        return Response(CartSerializer(cart).data)


class ClearCartView(CartMixin, APIView):
    """Clear all items from cart."""
    
    permission_classes = [permissions.AllowAny]
    
    def delete(self, request):
        cart = self.get_cart(request)
        
        # Track removal for all items
        for item in cart.items.all():
            track_interaction(
                request=request,
                product=item.product,
                interaction_type='remove_from_cart',
                metadata={'quantity': item.quantity, 'cart_cleared': True}
            )
        
        cart.items.all().delete()
        
        return Response(CartSerializer(cart).data)


class MergeCartView(CartMixin, APIView):
    """Merge anonymous cart with user cart after login."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        session_key = request.data.get('session_key')
        if not session_key:
            return Response({'message': 'No session key provided'})
        
        try:
            anonymous_cart = Cart.objects.get(session_key=session_key)
        except Cart.DoesNotExist:
            return Response({'message': 'No anonymous cart found'})
        
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Merge items
        for item in anonymous_cart.items.all():
            user_item, created = CartItem.objects.get_or_create(
                cart=user_cart,
                product=item.product,
                defaults={'quantity': item.quantity}
            )
            if not created:
                user_item.quantity += item.quantity
                user_item.save()
        
        # Delete anonymous cart
        anonymous_cart.delete()
        
        return Response(CartSerializer(user_cart).data)
