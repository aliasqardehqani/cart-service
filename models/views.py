from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import PartUnified, CartItem
from .serializers import PartUnifiedSerializer, CartItemSerializer
from .cart_service import CartService
from rest_framework.pagination import PageNumberPagination


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

class FinalizeOrderView(APIView):
    """
    Finalize the authenticated user's cart and create an order
    Sends confirmation email on success
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            order = CartService.finalize_order(request.user)
            return Response({'status': 'success', 'order_id': order.id}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
