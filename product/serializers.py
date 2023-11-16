from rest_framework import serializers
from product.models import Product, ProductImage, Category
from users.models import Seller


class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "url"]


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(required=True, many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "description",
            "created_on",
            "updated_on",
            "product_images",
            "category",
        ]

    def create(self, validated_data):
        product_images = validated_data.pop("product_images")
        user = self.context["user"]
        seller = Seller.objects.get(user=user)
        product = Product.objects.create(seller=seller, **validated_data)
        urls = [image.get("url") for image in product_images]
        ProductImage.objects.bulk_create(
            [ProductImage(url=url, product=product) for url in urls]
        )
        return product


class ProductSerializerRead(ProductSerializer):
    category = CategoryProductSerializer()
    product_images = ProductImageSerializer(required=True, many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "description",
            "created_on",
            "updated_on",
            "product_images",
            "category",
        ]


class ProductSerializerNoCategory(serializers.ModelSerializer):
    product_images = ProductImageSerializer(required=True, many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "description",
            "created_on",
            "updated_on",
            "product_images",
        ]


class ProductCategorySerializer(serializers.ModelSerializer):
    category_products = ProductSerializerNoCategory(many=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "category_products"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
