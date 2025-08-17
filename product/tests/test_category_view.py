# product/tests/test_category_views.py
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from product.models import Category

pytestmark = pytest.mark.django_db

class TestCategoryViewSet:
    endpoint = "/bookstore/v1/categories/"

    def test_list_categories(self):
        Category.objects.create(title="Eletrônicos", slug="eletronicos", description="Categoria de eletrônicos")
        client = APIClient()
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["title"] == "Eletrônicos"

    def test_create_category(self):
        client = APIClient()
        payload = {"title": "Livros", "slug": "livros", "description": "Categoria de livros"}
        response = client.post(self.endpoint, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.count() == 1

    def test_retrieve_category(self):
        category = Category.objects.create(title="Games", slug="games", description="Categoria de games")
        client = APIClient()
        response = client.get(f"{self.endpoint}{category.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Games"

    def test_update_category(self):
        category = Category.objects.create(title="Casa", slug="casa", description="Itens de casa")
        client = APIClient()
        payload = {"title": "Casa e Jardim", "slug": "casa-jardim", "description": "Atualizado"}
        response = client.put(f"{self.endpoint}{category.id}/", payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        category.refresh_from_db()
        assert category.title == "Casa e Jardim"

    def test_delete_category(self):
        category = Category.objects.create(title="Música", slug="musica", description="Categoria de música")
        client = APIClient()
        response = client.delete(f"{self.endpoint}{category.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Category.objects.count() == 0
