from django.contrib import admin
from .models import PartUnified

@admin.register(PartUnified)
class PartUnifiedAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'commercial_code', 
        'internal_code', 
        'price', 
        'category_title', 
        'part_type', 
        'turnover', 
        'inventory'
    )
    list_filter = (
        'part_type', 
        'turnover', 
        'category_title'
    )
    search_fields = (
        'name', 
        'commercial_code', 
        'internal_code', 
        'category_title',
        'description'
    )
    readonly_fields = ('image_preview',)
    fieldsets = (
        ("Part Details", {
            'fields': (
                'name', 'internal_code', 'commercial_code', 'price', 
                'cars', 'description', 'part_type', 'turnover', 'inventory'
            )
        }),
        ("Category Details", {
            'fields': (
                'category_title', 'category_url', 'category_description'
            )
        }),
        ("Images", {
            'fields': (
                'image_urls', 'image_preview',
            )
        }),
    )

    def image_preview(self, obj):
        if obj.image_urls:
            from django.utils.html import format_html
            html = ""
            for url in obj.image_urls:
                html += format_html('<img src="{}" style="height:50px; margin-right:5px;" />', url)
            return format_html(html)
        return "No Images"
    image_preview.short_description = "Image Preview"
