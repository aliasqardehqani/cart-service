from rest_framework import serializers
from .models import PartUnified

class PartUnifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartUnified
        fields = [
            'id', 'name', 'internal_code', 'commercial_code', 'price',
            'cars', 'description', 'category_title', 'category_url',
            'category_description', 'image_urls', 'part_type',
            'turnover', 'inventory'
        ]
