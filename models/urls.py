from django.urls import path
from .views import (
    PartUnifiedListView,
    AddItemToCartView,
    FinalizeOrderView,
    DeleteCartItemView, ClearCartView
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Product API
    path('parts/', PartUnifiedListView.as_view(), name='part-list'),

    # Cart API
    path('add/', AddItemToCartView.as_view(), name='cart-add'),
    path('list-cart/', AddItemToCartView.as_view(), name='cart-list'),
    path('finalize/', FinalizeOrderView.as_view(), name='cart-finalize'),
    path('delete/<int:item_id>/', DeleteCartItemView.as_view(), name='delete-cart-item'),
    path('clear/', ClearCartView.as_view(), name='clear-cart'),

]
