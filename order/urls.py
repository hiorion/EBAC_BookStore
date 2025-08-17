from django.urls import path, include
from rest_framework import routers
from order.viewsets.order_viewset import OrderViewSet

router = routers.SimpleRouter()
router.register(r'', OrderViewSet, basename='order')  # rota vazia, prefixo já vem do bookstore/urls.py

urlpatterns = [
    path('', include(router.urls)),
]
