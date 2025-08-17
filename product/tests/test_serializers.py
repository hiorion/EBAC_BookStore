# product/tests/test_serializers.py

import pytest
from product.serializers import CategorySerializer, ProductSerializer
from product.factories import CategoryFactory, ProductFactory

# ---------- CATEGORY SERIALIZER ----------
@pytest.mark.django_db
def test_category_serializer_output():
    category = CategoryFactory()
    data = CategorySerializer(category).data

    assert set(data.keys()) == {"id", "title", "slug", "description", "active"}
    assert data["title"] == category.title


# ---------- PRODUCT SERIALIZER ----------
@pytest.mark.django_db
def test_product_serializer_output():
    product = ProductFactory()
    data = ProductSerializer(product).data

    assert "id" in data
    assert "title" in data
    assert "price" in data
    assert "categories" in data
    assert data["title"] == product.title


@pytest.mark.django_db
def test_product_serializer_input_and_save():
    category1 = CategoryFactory()
    category2 = CategoryFactory()
    payload = {
        "title": "Livro Teste",
        "price": "49.90",
        "category_ids": [category1.id, category2.id],
    }

    serializer = ProductSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors

    product = serializer.save()
    assert product.title == "Livro Teste"
    assert float(product.price) == 49.90
    assert set(product.categories.all()) == {category1, category2}
