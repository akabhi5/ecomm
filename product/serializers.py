from rest_framework import serializers
from product.models import Product, ProductImage, Category
from brand.models import Brand
from users.models import Seller


class ProductBrand(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "url"]


class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
        ]


class ProductCartSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "product_images"]


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(required=True, many=True)
    brand = ProductBrand(read_only=True)

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
            "brand",
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
            "brand",
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


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "image",
        )  # Fields to include for subcategories


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "subcategories",
        )  # Fields to include for categories
