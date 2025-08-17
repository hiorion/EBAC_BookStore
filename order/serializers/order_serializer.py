from rest_framework import serializers
from order.models import Order
from product.models import Product
from product.serializers.product_serializer import ProductSerializer
from django.contrib.auth.models import User

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(source='product', many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        source='product',
        many=True,
        queryset=Product.objects.all(),
        write_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.all(),
        write_only=True
    )
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'products', 'product_ids', 'total']

    def get_total(self, instance):
        return sum(product.price for product in instance.product.all())

    def create(self, validated_data):
        products = validated_data.pop('product')
        user = validated_data.pop('user')
        order = Order.objects.create(user=user)
        order.product.set(products)
        return order
