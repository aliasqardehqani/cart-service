from django.urls import path
from .views import (
    PartUnifiedListView,
    AddItemToCartView,
    CreateOrderView,
    DeleteCartItemView, 
    ClearCartView
)

urlpatterns = [
    # Product API
    path('parts/', PartUnifiedListView.as_view(), name='part-list'),

    # Cart API
    path('add/', AddItemToCartView.as_view(), name='cart-add'),
    path('list-cart/', AddItemToCartView.as_view(), name='cart-list'),
    path('orders/create/', CreateOrderView.as_view(), name='create-order'),
    path('delete/<int:item_id>/', DeleteCartItemView.as_view(), name='delete-cart-item'),
    path('clear/', ClearCartView.as_view(), name='clear-cart'),

]
