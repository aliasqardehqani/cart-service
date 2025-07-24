from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import PartUnified
from .cart_service import CartService
from rest_framework import generics
from .serializers import PartUnifiedSerializer

# @login_required
def add_item_to_cart(request, part_id):
    part = PartUnified.objects.get(id=part_id)
    CartService.add_to_cart(request.user, part, quantity=1)
    return JsonResponse({'status': 'added'})

# @login_required
def finalize_order(request):
    try:
        order = CartService.finalize_order(request.user)
        return JsonResponse({'status': 'success', 'order_id': order.id})
    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)})



class PartUnifiedListView(generics.ListAPIView):
    queryset = PartUnified.objects.all()
    serializer_class = PartUnifiedSerializer
