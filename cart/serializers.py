from rest_framework import serializers
from cart.models import Cart, CartItem
from product.models import Product
from product.serializers import ProductCartSerializer
from users.models import Customer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "quantity", "product", "size"]


class CartItemWriteSerializer(serializers.ModelSerializer):
    product_slug = serializers.CharField(write_only=True)
    product = ProductCartSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "quantity", "product_slug", "product", "size"]

    def create(self, validated_data: dict):
        user = self.context["user"]
        customer = Customer.objects.get(user=user)
        product_slug = validated_data.pop("product_slug")
        size = validated_data.get("size")
        product = Product.objects.filter(slug=product_slug)
        if not product.exists():
            raise serializers.ValidationError("Product does not exist.")
        product = product.first()

        record = CartItem.objects.filter(
            cart=customer.customer_cart, product=product, size=size
        )

        # if product in cart exist with same size then increase quantity
        if record.exists():
            record = record.first()
            record.quantity += 1
            record.save()
            return record
        else:  # otherwise add as new item
            return CartItem.objects.create(
                cart=customer.customer_cart, product=product, **validated_data
            )


class ChangeProductQuantityCartSerializer(serializers.ModelSerializer):
    product = ProductCartSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "quantity", "product", "size"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value

    def update(self, instance: CartItem, validated_data):
        quantity = validated_data.get("quantity")
        instance.quantity = quantity
        instance.save()
        return instance
