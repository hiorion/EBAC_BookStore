from django.urls import path, include
from rest_framework import routers
from product.viewsets.product_viewset import ProductViewSet

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet, basename='product')  # plural

urlpatterns = [
    path('', include(router.urls)),
]
