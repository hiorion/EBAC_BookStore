# product/factories.py
import factory
from product.models import Product, Category

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Faker("word")
    description = factory.Faker("sentence")
    price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    active = True

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        """
        Adiciona categorias após criar o produto.
        Exemplo de uso:
            cat1 = Category.objects.create(title="Cat1", slug="cat1")
            cat2 = Category.objects.create(title="Cat2", slug="cat2")
            ProductFactory(categories=[cat1, cat2])
        """
        if not create or not extracted:
            return
        for category in extracted:
            self.categories.add(category)
