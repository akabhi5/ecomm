from rest_framework import serializers

from product.serializers import ProductSerializer
from .models import Brand
from users.models import Seller


class BrandSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Brand
        fields = ["id", "name", "image", "description", "slug", "seller"]

    def create(self, validated_data: dict):
        user = self.context["user"]
        seller = Seller.objects.get(user=user)
        return Brand.objects.create(seller=seller, **validated_data)


class BrandProductSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(read_only=True)
    brand_products = ProductSerializer(many=True)

    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "image",
            "description",
            "slug",
            "seller",
            "brand_products",
        ]
