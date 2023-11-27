from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart, CartItem
from cart.serializers import AddProductToCartSerializer, CartSerializer
from users.models import Customer

from users.permissions import IsCustomer


def get_customer_cart(customer):
    cart = Cart.objects.get(customer=customer)
    serializer = CartSerializer(cart)
    return serializer.data


class CartView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request, format=None):
        user = request.user
        customer = Customer.objects.get(user=user)
        cart, _ = Cart.objects.get_or_create(customer=customer)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request, format=None):
        customer = Customer.objects.get(user=request.user)
        serializer = AddProductToCartSerializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            serializer.save()
            cart = get_customer_cart(customer)
            return Response(cart, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailView(APIView):
    def delete(self, request, product, format=None):
        customer = Customer.objects.get(user=request.user)
        cart_item = CartItem.objects.filter(
            cart__customer=customer, product__slug=product
        )
        if cart_item.exists():
            cart_item.delete()
        cart = get_customer_cart(customer)
        return Response(cart, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, product, format=None):
        customer = Customer.objects.get(user=request.user)
        cart_item = CartItem.objects.filter(
            cart__customer=customer, product__slug=product
        )
        if cart_item.exists():
            cart_item.delete()
        cart = get_customer_cart(customer)
        return Response(cart, status=status.HTTP_204_NO_CONTENT)
