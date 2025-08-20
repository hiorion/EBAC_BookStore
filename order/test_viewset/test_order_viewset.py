# order/test_viewset/test_order_viewset.py

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from product.factories import ProductFactory
from order.models import Order

class TestOrderSerializer(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="henry", password="123456")

        self.product1 = ProductFactory(title="mouse", price=100)
        self.product2 = ProductFactory(title="keyboard", price=150)

        # URL versionada da API
        self.list_url = "/bookstore/v1/order/"
        self.create_url = "/bookstore/v1/order/"

    def test_create_order(self):
        data = {
            "user_id": self.user.id,
            "product_ids": [self.product1.id, self.product2.id]
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.get(user=self.user)
        self.assertEqual(order.product.count(), 2)  # <-- singular
        self.assertIn(self.product1, order.product.all())
        self.assertIn(self.product2, order.product.all())

        self.assertEqual(response.data["total"], 250)

    def test_list_orders(self):
        order = Order.objects.create(user=self.user)
        order.product.add(self.product1, self.product2)  # <-- singular
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["total"], 250)
        self.assertEqual(len(response.data[0]["products"]), 2)
        self.assertIn("mouse", [p["title"] for p in response.data[0]["products"]])
