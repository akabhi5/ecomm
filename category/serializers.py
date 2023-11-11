from rest_framework import serializers

from category.models import Category
from product.serializers import ProductSerializerNoCategory


class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
        ]


class CategorySerializer(serializers.ModelSerializer):
    category_products = ProductSerializerNoCategory(many=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "category_products"]
