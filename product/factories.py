# product/factories.py

import factory
from product.models import Product, Category

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Faker("word")
    slug = factory.Faker("slug")
    description = factory.Faker("sentence")
    active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        skip_postgeneration_save = True  # <-- Adicione isso para remover o warning

    title = factory.Faker("word")
    description = factory.Faker("sentence")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    active = True

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for category in extracted:
            self.categories.add(category)
