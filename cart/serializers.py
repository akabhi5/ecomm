from rest_framework import serializers
from cart.models import Cart, CartItem
from product.models import Product
from product.serializers import CategoryProductSerializer
from users.models import Customer


class CartItemSerializer(serializers.ModelSerializer):
    product = CategoryProductSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "quantity", "product"]


class CartItemWriteSerializer(serializers.ModelSerializer):
    product_slug = serializers.CharField(write_only=True)
    product = CategoryProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "quantity", "product_slug", "product"]

    def create(self, validated_data: dict):
        user = self.context["user"]
        if not Cart.objects.filter(customer__user=user).exists():
            Cart.objects.create(customer=user.customer)
        customer = Customer.objects.get(user=user)
        product_slug = validated_data.pop("product_slug")
        product = Product.objects.get(slug=product_slug)
        print(validated_data)
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
