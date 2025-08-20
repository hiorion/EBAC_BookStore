import factory
from django.contrib.auth.models import User
from product.models import Category, Product
from order.models import Order

# ---------- CATEGORY ----------
class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("word")
    slug = factory.Faker("slug")
    description = factory.Faker("sentence")
    active = factory.Iterator([True, False])

    class Meta:
        model = Category


# ---------- PRODUCT ----------
class ProductFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("word")
    price = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )
    # Removi o category porque não existe no modelo Product
    # category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Product


# ---------- USER ----------
class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    username = factory.Faker("user_name")

    class Meta:
        model = User


# ---------- ORDER ----------
class OrderFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        """
        Permite adicionar produtos ao criar o pedido:
        OrderFactory(products=[p1, p2, p3])
        """
        if not create:
            return

        if extracted:
            for product in extracted:
                self.product.add(product)  # Corrigido para 'product' e não 'products'

    class Meta:
        model = Order
