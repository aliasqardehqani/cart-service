from rest_framework import serializers
from .models import PartUnified, CartItem, Person, Order

class PartUnifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartUnified
        fields = [
            'id', 'name', 'internal_code', 'commercial_code', 'price',
            'cars', 'description', 'category_title', 'category_url',
            'category_description', 'image_urls', 'part_type',
            'turnover', 'inventory'
        ]

class CartItemSerializer(serializers.ModelSerializer):
    part = PartUnifiedSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'part', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=CartItem.objects.all())

    class Meta:
        model = Order
        fields = ['user', 'post_type', 'delivery_date', 'total_price', 'items', 'order_code']
        read_only_fields = ['order_code']

    def create(self, validated_data):
        items = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        order.items.set(items)
        return order
    
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['full_name', 'phone_number', 'email', 'postal_code', 'address']