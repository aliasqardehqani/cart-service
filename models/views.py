from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import PartUnified, CartItem, Person, Order
from .serializers import PartUnifiedSerializer, CartItemSerializer, OrderSerializer
from .cart_service import CartService
from rest_framework.pagination import PageNumberPagination
import datetime

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def generate_invoice(order: Order) -> str:
    """
    Generate a simple invoice text for the given order.
    """
    lines = []
    lines.append(f"فاکتور سفارش")
    lines.append(f"کد سفارش: {order.order_code}")
    lines.append(f"نام کاربر: {order.user.username}")
    lines.append(f"تاریخ ایجاد سفارش: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"نوع ارسال: {order.get_post_type_display()}")
    lines.append(f"تاریخ تحویل: {order.delivery_date if order.delivery_date else 'تعریف نشده'}")
    lines.append(f"مجموع قیمت: {order.total_price:,} تومان")
    lines.append("")
    lines.append("آیتم‌ها:")

    for item in order.items.all():
        part_name = item.part.name if hasattr(item, 'part') else "نامشخص"
        quantity = item.quantity
        price = item.part.price if hasattr(item, 'part') else 0
        total_item_price = price * quantity
        lines.append(f"- {part_name} | تعداد: {quantity} | قیمت واحد: {price:,} | قیمت کل: {total_item_price:,}")

    lines.append("")
    lines.append("با تشکر از خرید شما.")

    return "\n".join(lines)

def send_to_phone(phone, message):
    print(message)

def payment_gateway(phone):
    return True

class StandardResultsSetPagination(PageNumberPagination):
    # Default page size
    page_size = 50
    # Allow client to set page size using query parameter
    page_size_query_param = 'page_size'
    # Maximum allowed page size
    max_page_size = 200
    # Page number parameter (default is "page")
    page_query_param = 'page'


class PartUnifiedListView(APIView):
    """
    Return a paginated list of products (PartUnified)
    Accepts query parameters: ?page=1&page_size=50
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Load only necessary fields to reduce DB load
        queryset = PartUnified.objects.only(
            'id', 'name', 'commercial_code', 'price',
            'part_type', 'inventory'
        ).order_by('id')

        # Apply pagination based on client input
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = PartUnifiedSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

class AddItemToCartView(APIView):
    """
    Add product to cart with specific quantity and update product stock.
    """

    def post(self, request):
        part_id = request.data.get('part_id')
        quantity = int(request.data.get('quantity', 1))  
        user = request.user
        part = get_object_or_404(PartUnified, id=part_id)

        quantity = int(request.data.get('quantity', 1))  

        if quantity < 1:
            return Response({'error': 'Quantity must be at least 1.'}, status=400)

        if part.inventory < quantity:
            return Response({'error': 'Not enough stock available.'}, status=400)

        CartService.add_to_cart(user, part, quantity=quantity)

        part.inventory -= quantity
        part.save()

        return Response({'message': f'{quantity} عدد از محصول به سبد خرید اضافه شد.'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        cart = CartService.get_or_create_cart(user)
        items = cart.items.all()
        serializer = CartItemSerializer(items, many=True)

        total_price = sum(item.part.price * item.quantity for item in items)

        response_data = {
            'items': serializer.data,
            'total_price': total_price,
        }

        if items.count() < 20:
            response_data['message'] = 'برای مشاوره با شماره +989386678858 تماس بگیرید.'

        return Response(response_data, status=200)



class CreateOrderView(APIView):
    """
    API endpoint for creating a new order from user's cart.
    """

    def post(self, request):
        user = request.user

        # 1. Check if user has a saved Person info
        person = Person.objects.filter(email=user.email).order_by('-created_at').first()
        if not person:
            return Response({'error': 'User info not found. Please complete your profile.'}, status=400)

        # 2. Validate required fields
        missing_fields = []
        if not person.postal_code:
            missing_fields.append("کد پستی ثبت نشده")
        if not person.address:
            missing_fields.append("آدرس ثبت نشده")
        if not person.email:
            missing_fields.append("ایمیل ثبت نشده")

        if missing_fields:
            return Response({'error': missing_fields}, status=400)

        # 3. Get cart items
        cart = CartService.get_or_create_cart(user)
        items = cart.items.all()

        if not items.exists():
            return Response({'error': 'Your cart is empty.'}, status=400)

        # 4. Parse delivery timestamp
        try:
            timestamp = int(request.data.get("delivery_date"))
            delivery_date = datetime.datetime.fromtimestamp(timestamp).date()
        except (TypeError, ValueError):
            return Response({'error': 'Invalid delivery_date timestamp.'}, status=400)

        # 5. Calculate total price
        total_price = sum(item.part.price * item.quantity for item in items)

        # 6. Prepare data for serializer (بدون ارسال items)
        serializer = OrderSerializer(data={
            'user': user.id,
            'post_type': request.data.get('post_type'),
            'delivery_date': delivery_date,
            'total_price': total_price,
            'items': [item.pk for item in items],
            'order_status': 'waiting'
        })
          
        if serializer.is_valid():
            serializer.save()
            cart.items.all().delete()

            return Response({
                'order': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentGatewayView(APIView):
    def post(self, request):
        order_code = request.data.get('order_code')
        print(order_code)
        return Response({"message": "success"}, status=status.HTTP_200_OK)

class PaymentWebhookAPIView(APIView):
    """
    API view to handle payment gateway webhook callbacks.
    Updates the order status based on payment result.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        # Disable CSRF check for webhook endpoint
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        user = request.user
        # Get the order ID from POST data sent by the payment gateway
        order_code = request.data.get('order_code')
        # Get the payment status from POST data, e.g. "success" or "failed"
        payment_status = request.data.get('status')

        # Retrieve the order object or return 404 if not found
        order = get_object_or_404(Order, order_code=order_code)

        # Update order status based on payment result
        if payment_status == "success":
            order.order_status = "paied"  # Note: spelling as per your choices
            order.save()
            # TODO: send confirmation email or SMS to the user 
            invoice_text = generate_invoice(order)
            # send_to_phone(user.phone_number, invoice_text)
            content = {
                'invoice': invoice_text
            }
        else:
            order.order_status = "failed"
            order.save()
            content = {
                'Message': 'Your payment is failed'
            }
        # Return simple HTTP 200 OK response to acknowledge webhook receipt
        return Response(content, status=status.HTTP_200_OK)

class DeleteCartItemView(APIView):
    """
    Delete a specific item from user's cart.
    """

    def delete(self, request, item_id):
        user = request.user
        item = get_object_or_404(CartItem, id=item_id, cart__user=user)
        item.delete()
        return Response({'message': 'آیتم با موفقیت حذف شد.'}, status=status.HTTP_204_NO_CONTENT)
    
class ClearCartView(APIView):
    """
    Clear all items in the user's cart.
    """

    def delete(self, request):
        user = request.user
        cart = CartService.get_or_create_cart(user)
        cart.items.all().delete()
        return Response({'message': 'سبد خرید با موفقیت پاک شد.'}, status=status.HTTP_204_NO_CONTENT)
