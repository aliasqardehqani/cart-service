from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class PartUnified(models.Model):
    """
    Unified model combining Part, PartCategory, and PartImage information.
    Represents a car part with its codes, price, category details, 
    and associated images.
    """
    PART_TYPE_CHOICES = (
        ('consumable', 'Consumable'),  
        ('spare', 'Spare Part'),       
    )

    TURNOVER_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    # Part fields
    name = models.CharField(max_length=255)
    internal_code = models.CharField(max_length=50)
    commercial_code = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    cars = models.TextField()
    description = models.TextField(blank=True, null=True)

    # PartCategory fields
    category_title = models.CharField(max_length=255)
    category_url = models.URLField()
    category_description = models.TextField(blank=True, null=True)

    # category = models.ForeignKey(
    #     PartCategory,
    #     on_delete=models.CASCADE,
    #     related_name='parts',
    #     null=True, 
    #     blank=True
    # )

    # PartImage fields
    image_urls = models.JSONField(blank=True, null=True, help_text="List of image URLs related to the part category")

    part_type = models.CharField(
        max_length=20,
        choices=PART_TYPE_CHOICES,
        default='spare',
        help_text="Specify whether the part is a consumable item or a spare part"
    )

    # New fields
    turnover = models.CharField(
        max_length=1,
        choices=TURNOVER_CHOICES,
        blank=True,
        null=True,
        help_text="Product turnover category: A, B, C, or D"
    )
    inventory = models.IntegerField(
        default=0,
        help_text="Current inventory count for the part"
    )

    def __str__(self):
        return f"{self.name} - {self.commercial_code} - Category: {self.category_title}"


# -------------------------------------------


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    part = models.ForeignKey(PartUnified, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def total_price(self):
        return self.part.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.part.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

