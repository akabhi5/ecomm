from rest_framework import serializers
from category.serializers import CategorySerializer
from product.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "url"]


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(required=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "created_on",
            "updated_on",
            "product_images",
            "category",
        ]

    def create(self, validated_data):
        product_images = validated_data.pop("product_images")
        product = Product.objects.create(**validated_data)
        urls = [image.get("url") for image in product_images]
        ProductImage.objects.bulk_create(
            [ProductImage(url=url, product=product) for url in urls]
        )
        return product
