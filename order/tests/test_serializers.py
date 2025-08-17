import pytest
from order.factories import OrderFactory, ProductFactory
from order.serializers import OrderSerializer

@pytest.mark.django_db
def test_order_serializer_output():
    product1 = ProductFactory(price=100.00)
    product2 = ProductFactory(price=50.00)

    order = OrderFactory()
    order.product.set([product1, product2])

    serializer = OrderSerializer(order)

    data_products = serializer.data["products"]

    # Verifica se todos os produtos estão presentes e têm os preços corretos
    prices = {prod["id"]: prod["price"] for prod in data_products}
    assert product1.id in prices
    assert product2.id in prices
    assert prices[product1.id] == "100.00"
    assert prices[product2.id] == "50.00"
