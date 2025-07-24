from django.contrib import admin
from .models import PartUnified, Cart, CartItem, Order, Person


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






@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'part', 'quantity', 'total_price')
    list_filter = ('cart', 'part')
    search_fields = ('part__name', 'cart__user__username')
    raw_id_fields = ('cart', 'part')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('total_price',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price_display')
    search_fields = ('user__username',)
    inlines = [CartItemInline]

    def total_price_display(self, obj):
        return obj.total_price()
    total_price_display.short_description = "Total Price"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    filter_horizontal = ('items',)



@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'postal_code', 'created_at')
    search_fields = ('full_name', 'phone_number', 'email', 'postal_code')
    list_filter = ('created_at',)
    ordering = ('-created_at',)