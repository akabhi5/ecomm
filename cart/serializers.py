from rest_framework import serializers
from cart.models import Cart, CartItem
from product.models import Product
from product.serializers import CategoryProductSerializer, ProductCartSerializer
from users.models import Customer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "quantity", "product"]


class CartItemWriteSerializer(serializers.ModelSerializer):
    product_slug = serializers.CharField(write_only=True)
    product = CategoryProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "quantity", "product_slug", "product"]

    def validate_product_slug(self, value):
        user = self.context["user"]
        customer = Customer.objects.get(user=user)
        if CartItem.objects.filter(
            product__slug=value, cart__customer__user=customer
        ).exists():
            raise serializers.ValidationError("Product already in cart.")
        return value

    def create(self, validated_data: dict):
        user = self.context["user"]
        customer = Customer.objects.get(user=user)
        product_slug = validated_data.pop("product_slug")
        product = Product.objects.filter(slug=product_slug)
        if not product.exists():
            raise serializers.ValidationError("Product does not exist.")
        product = product.first()
        return CartItem.objects.create(
            cart=customer.customer_cart, product=product, **validated_data
        )


class ChangeProductQuantityCartSerializer(serializers.ModelSerializer):
    product = CategoryProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "quantity", "product"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value

    def update(self, instance: CartItem, validated_data):
        quantity = validated_data.get("quantity")
        instance.quantity = quantity
        instance.save()
        return instance
