from django.db import models
from django.contrib.auth.models import User



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
    cars = models.ManyToManyField('CarsModel', related_name="parts")
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
