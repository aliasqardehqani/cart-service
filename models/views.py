from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import PartUnified
from .serializers import PartUnifiedSerializer
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
    Add a product to the authenticated user's cart
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, part_id):
        part = get_object_or_404(PartUnified, id=part_id)
        CartService.add_to_cart(request.user, part, quantity=1)
        return Response({'status': 'added'}, status=status.HTTP_200_OK)


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
