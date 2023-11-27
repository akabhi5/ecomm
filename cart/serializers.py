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


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "customer", "cart_items"]


class AddProductToCartSerializer(serializers.Serializer):
    product = serializers.SlugField()

    def validate_product_slug(self, value):
        product = Product.objects.filter(slug=value)
        if not product.exists():
            raise serializers.ValidationError("Invalid product")
        return value

    def create(self, validated_data):
        product_slug = validated_data["product"]
        product = Product.objects.get(slug=product_slug)
        user = self.context["user"]
        customer = Customer.objects.get(user=user)
        cart_item_exists = CartItem.objects.filter(
            cart__customer=customer, product=product
        ).exists()
        if cart_item_exists:
            raise serializers.ValidationError("Product already added to cart")
        cart_item = CartItem.objects.create(
            cart=customer.customer_cart, product=product, quantity=1
        )
        return cart_item


class ChangeProductQuantityToCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
