from rest_framework import serializers
from main.models import Product, Menu


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field="name")
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "description", "weight", "category", "price", "image"]

    def get_price(self, obj):
        return int(obj.price)


class MenuSerializer(serializers.ModelSerializer):
	products = ProductSerializer(many=True, read_only=True)

	class Meta:
		model = Menu
		fields = ["id", "name", "slug", "products"]
