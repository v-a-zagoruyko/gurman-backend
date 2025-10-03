import uuid
import factory
from decimal import Decimal
from django.utils import timezone
from main.models import AuthToken, Category, Product, Menu


class AuthTokenFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = AuthToken

	token = factory.Sequence(lambda n: str(uuid.uuid4()))


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")


class ProductFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Product

	name = factory.Sequence(lambda n: f"Product {n}")
	price = Decimal('100.00')
	category = factory.SubFactory(CategoryFactory)
	description = "Some description"
	weight = "1 kg"


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu
        skip_postgeneration_save = True

    name = factory.Sequence(lambda n: f"Menu {n}")

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                self.products.add(product)
