from rest_framework import serializers
from product.models import Product, ProductImage, Category, ProductSizeQuantity
from brand.models import Brand
from users.models import Seller


class ProductSizeQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizeQuantity
        fields = ["xs", "s", "m", "l", "xl"]


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
    size_quantity = ProductSizeQuantitySerializer(required=False)

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
            "size_quantity",
        ]

    def create(self, validated_data):
        product_images = validated_data.pop("product_images")
        user = self.context["user"]
        seller = Seller.objects.get(user=user)
        size_quantity = validated_data.pop("size_quantity")
        product = Product.objects.create(seller=seller, **validated_data)
        product_size_quantity = ProductSizeQuantity.objects.create(
            product_id=product.id, **size_quantity
        )
        urls = [image.get("url") for image in product_images]
        ProductImage.objects.bulk_create(
            [ProductImage(url=url, product=product) for url in urls]
        )
        product.size_quantity = product_size_quantity
        return product

    def update(self, instance, validated_data):
        # delete all image for this product
        images_to_delete = ProductImage.objects.filter(product=instance)
        for img in images_to_delete:
            img.delete()

        # add new product
        product_images = validated_data.pop("product_images")
        urls = [image.get("url") for image in product_images]
        ProductImage.objects.bulk_create(
            [ProductImage(url=url, product=instance) for url in urls]
        )

        instance.name = validated_data.get("name", instance.name)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.brand = validated_data.get("brand", instance.brand)
        instance.category = validated_data.get("category", instance.category)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)

        size_quantity = validated_data.pop("size_quantity")
        psq = ProductSizeQuantity.objects.get(product=instance)
        psq.xs = size_quantity.get("xs", psq.xs)
        psq.s = size_quantity.get("s", psq.s)
        psq.m = size_quantity.get("m", psq.m)
        psq.l = size_quantity.get("l", psq.l)
        psq.xl = size_quantity.get("xl", psq.xl)
        psq.save()

        instance.save()
        return instance


class ProductSerializerRead(ProductSerializer):
    category = CategoryProductSerializer()
    product_images = ProductImageSerializer(required=True, many=True)
    brand = ProductBrand(read_only=True)
    size_quantity = ProductSizeQuantitySerializer()

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
            "size_quantity",
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
