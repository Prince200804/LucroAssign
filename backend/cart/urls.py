from django.urls import path
from .views import (
    CartView, AddToCartView, UpdateCartItemView,
    RemoveFromCartView, ClearCartView, MergeCartView
)

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('update/<uuid:item_id>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('remove/<uuid:item_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('clear/', ClearCartView.as_view(), name='clear-cart'),
    path('merge/', MergeCartView.as_view(), name='merge-cart'),
]
