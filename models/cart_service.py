from django.core.mail import send_mail
from django.conf import settings
from .models import Cart, CartItem, Order


class CartService:
    @staticmethod
    def get_or_create_cart(user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    def add_to_cart(user, part, quantity=1):
        cart = CartService.get_or_create_cart(user)
        item, created = CartItem.objects.get_or_create(cart=cart, part=part)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        return item

    @staticmethod
    def remove_from_cart(user, part):
        cart = CartService.get_or_create_cart(user)
        CartItem.objects.filter(cart=cart, part=part).delete()

    @staticmethod
    def clear_cart(user):
        cart = CartService.get_or_create_cart(user)
        cart.items.all().delete()

    @staticmethod
    def finalize_order(user):
        cart = CartService.get_or_create_cart(user)
        if not cart.items.exists():
            raise ValueError("Cart is empty.")

        total = cart.total_price()
        order = Order.objects.create(user=user, total_price=total)
        order.items.set(cart.items.all())
        order.save()

        CartService.send_order_email(user, order)
        CartService.clear_cart(user)

        return order

    @staticmethod
    def send_order_email(user, order):
        subject = f"Order Confirmation #{order.id}"
        message = f"Dear {user.username},\n\nYour order has been placed successfully.\nTotal price: {order.total_price}.\n\nThank you for shopping!"
        recipient = [user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient)
