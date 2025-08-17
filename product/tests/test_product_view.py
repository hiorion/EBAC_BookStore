import pytest
from rest_framework.test import APIClient
from rest_framework import status
from product.models import Product, Category

pytestmark = pytest.mark.django_db

class TestProductViewSet:
    endpoint = "/bookstore/v1/products/"  # plural, combinando com router

    def test_create_product_with_category(self):
        category = Category.objects.create(title="Tech", slug="tech", description="Tecnologia")
        client = APIClient()
        payload = {
            "title": "Notebook",
            "description": "Um notebook gamer",
            "price": "4500.00",
            "active": True,
            "category_ids": [category.id]
        }
        response = client.post(self.endpoint, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        product = Product.objects.first()
        assert product.categories.filter(id=category.id).exists()

    def test_list_products(self):
        Product.objects.create(title="Celular", description="Smartphone", price="2000.00", active=True)
        client = APIClient()
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["title"] == "Celular"

    def test_retrieve_product(self):
        product = Product.objects.create(title="TV", description="Smart TV", price="3000.00", active=True)
        client = APIClient()
        response = client.get(f"{self.endpoint}{product.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "TV"

    def test_update_product(self):
        product = Product.objects.create(title="Mouse", description="Mouse gamer", price="150.00", active=True)
        client = APIClient()
        payload = {"title": "Mouse Wireless", "description": "Mouse sem fio", "price": "180.00", "active": True, "category_ids": []}
        response = client.put(f"{self.endpoint}{product.id}/", payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        product.refresh_from_db()
        assert product.title == "Mouse Wireless"

    def test_delete_product(self):
        product = Product.objects.create(title="Teclado", description="Teclado mecânico", price="250.00", active=True)
        client = APIClient()
        response = client.delete(f"{self.endpoint}{product.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Product.objects.count() == 0
