from rest_framework import serializers
from main.models import Product, Menu


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Product
        fields = ["id", "name", "weight", "category", "price", "image"]


class MenuSerializer(serializers.ModelSerializer):
	products = ProductSerializer(many=True, read_only=True)

	class Meta:
		model = Menu
		fields = ["id", "name", "slug", "products"]
