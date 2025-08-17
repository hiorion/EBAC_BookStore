import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from product.models import Product
from order.models import Order

@pytest.mark.django_db
class TestOrderViewSet:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='henry', password='1234')
        self.product1 = Product.objects.create(title='Livro 1', price=50, active=True)
        self.product2 = Product.objects.create(title='Livro 2', price=70, active=True)
        self.url = reverse('order-list')

    def test_create_order(self):
        data = {
            'user_id': self.user.id,
            'product_ids': [self.product1.id, self.product2.id]
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 201
        assert response.data['total'] == 120

    def test_list_orders(self):
        order = Order.objects.create(user=self.user)
        order.product.set([self.product1, self.product2])
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_retrieve_order(self):
        order = Order.objects.create(user=self.user)
        order.product.set([self.product1])
        url = reverse('order-detail', args=[order.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data['total'] == self.product1.price

    def test_update_order(self):
        order = Order.objects.create(user=self.user)
        order.product.set([self.product1])
        data = {
            'product_ids': [self.product2.id]
        }
        url = reverse('order-detail', args=[order.id])
        response = self.client.patch(url, data, format='json')
        assert response.status_code == 200
        assert response.data['total'] == self.product2.price

    def test_delete_order(self):
        order = Order.objects.create(user=self.user)
        order.product.set([self.product1])
        url = reverse('order-detail', args=[order.id])
        response = self.client.delete(url)
        assert response.status_code == 204
        assert Order.objects.filter(id=order.id).count() == 0
