# product/tests_viewset/test_product_viewset.py

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from product.models import Product, Category

class ProductViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Criando algumas categorias
        self.cat1 = Category.objects.create(title="Categoria 1", slug="cat1")
        self.cat2 = Category.objects.create(title="Categoria 2", slug="cat2")

        # URLs com versionamento da API
        self.list_url = "/bookstore/v1/product/"
        self.create_url = "/bookstore/v1/product/"

    def test_list_products(self):
        # Criar produto para testar GET
        product = Product.objects.create(
            title="Produto 1",
            description="Descrição do produto",
            price="100.00",
            active=True
        )
        product.categories.add(self.cat1, self.cat2)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Produto 1")

    def test_create_product_with_categories(self):
        payload = {
            "title": "Produto Teste",
            "description": "Descrição teste",
            "price": "99.90",
            "active": True,
            "category_ids": [self.cat1.id, self.cat2.id]
        }
        response = self.client.post(self.create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product = Product.objects.get(title="Produto Teste")
        self.assertEqual(product.categories.count(), 2)
        self.assertIn(self.cat1, product.categories.all())
        self.assertIn(self.cat2, product.categories.all())
