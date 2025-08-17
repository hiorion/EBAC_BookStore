# product/serializers/product_serializer.py

from rest_framework import serializers
from product.models import Product, Category
from .category_serializer import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        write_only=True,
        source='categories'
    )

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "active", "categories", "category_ids"]
