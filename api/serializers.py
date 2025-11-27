from rest_framework import serializers
from main.models import Menu


class MenuSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ["id", "name", "slug", "products"]

    def get_products(self, obj):
        request = self.context.get("request")
        items = obj.items.select_related("product", "product__category").all()
        return [
            {
                "id": item.product.id,
                "name": item.product.name,
                "description": item.product.description,
                "weight": item.product.weight,
                "category": item.product.category.name if item.product.category else None,
                "price": int(item.price),
                "image": request.build_absolute_uri(item.product.image.url) if item.product.image else None,
            }
            for item in items
        ]
