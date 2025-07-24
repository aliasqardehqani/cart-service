from django.urls import path
from .views import (
    PartUnifiedListView,
    AddItemToCartView,
    FinalizeOrderView,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Product API
    path('api/parts/', PartUnifiedListView.as_view(), name='part-list'),

    # Cart API
    path('api/cart/add/<int:part_id>/', AddItemToCartView.as_view(), name='cart-add'),
    path('api/cart/finalize/', FinalizeOrderView.as_view(), name='cart-finalize'),

]
