from django.urls import path
from .views import *


urlpatterns = [
    path("add-to-cart/", add_item_to_cart, name="add-to-cart")
    path("order-cart/", finalize_order, name="order-cart")
]

