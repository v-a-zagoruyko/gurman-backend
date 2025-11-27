from rest_framework import serializers
from main.models import Menu
from django.conf import settings


class MenuSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ["id", "name", "slug", "products"]

    def get_products(self, obj):
        items = obj.items.select_related("product", "product__category").all()
        return [
            {
                "id": item.product.id,
                "name": item.product.name,
                "description": item.product.description,
                "weight": item.product.weight,
                "category": item.product.category.name if item.product.category else None,
                "price": int(item.price),
                "image": f"{settings.MEDIA_HOST}{item.product.image.url}" if item.product.image else None,
            }
            for item in items
        ]
