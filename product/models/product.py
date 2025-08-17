from django.db import models
from product.models import Category


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, related_name="products")