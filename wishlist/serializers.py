from rest_framework import serializers
from product.models import Product
from product.serializers import ProductCartSerializer
from users.models import Customer
from wishlist.models import Wishlist, WishlistItem


class WishListItemSerializer(serializers.ModelSerializer):
    product = ProductCartSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ["id", "wishlist", "product"]


class WishlistItemWriteSerializer(serializers.ModelSerializer):
    product_slug = serializers.CharField(write_only=True)
    product = ProductCartSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ["id", "product_slug", "product"]

    def validate_product_slug(self, value):
        user = self.context["user"]
        customer = Customer.objects.get(user=user)
        if WishlistItem.objects.filter(
            product__slug=value, wishlist__customer__user=customer
        ).exists():
            raise serializers.ValidationError("Product already in wishlist.")
        return value

    def create(self, validated_data: dict):
        user = self.context["user"]
        customer = Customer.objects.get(user=user)
        product_slug = validated_data.pop("product_slug")
        product = Product.objects.filter(slug=product_slug)
        if not product.exists():
            raise serializers.ValidationError("Product does not exist.")
        product = product.first()
        return WishlistItem.objects.create(
            wishlist=customer.customer_wishlist, product=product, **validated_data
        )
