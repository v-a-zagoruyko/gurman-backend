import uuid
import factory
from decimal import Decimal
from django.utils import timezone
from main.models import AuthToken, Category, Product, Menu, MenuItem


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
	category = factory.SubFactory(CategoryFactory)
	description = "Some description"
	weight = "1 kg"


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu

    name = factory.Sequence(lambda n: f"Menu {n}")


class MenuItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MenuItem

    menu = factory.SubFactory(MenuFactory)
    product = factory.SubFactory(ProductFactory)
    price = Decimal('100.00')
