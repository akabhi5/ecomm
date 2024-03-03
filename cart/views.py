from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from cart.models import CartItem
from cart.serializers import (
    CartItemSerializer,
    CartItemWriteSerializer,
    ChangeProductQuantityCartSerializer,
)
from users.permissions import IsCustomer


class CartItemsView(generics.ListCreateAPIView):
    permission_classes = [IsCustomer]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__customer__user=user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CartItemSerializer
        else:
            return CartItemWriteSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}


class CartItemsUpdateView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["patch", "delete"]
    permission_classes = [IsCustomer]
    lookup_field = "product__slug"  # this will be used for query
    lookup_url_kwarg = "product_slug"  # this will be used in url
    # if both are same then just use : 'lookup_field'

    def get_queryset(self):
        user = self.request.user
        product_slug = self.kwargs["product_slug"]
        size = self.kwargs["size"]
        return CartItem.objects.filter(
            cart__customer__user=user, product__slug=product_slug, size=size
        )

    def get_serializer_class(self):
        return ChangeProductQuantityCartSerializer


class CartTotalAmount(APIView):
    permission_classes = [IsCustomer]

    def get(self, request, format=None):
        cart = CartItem.objects.filter(cart__customer__user=request.user)
        cart_data = {}
        total_price = 0
        product_info = []
        for cart_item in cart:
            item_price = float(cart_item.product.price * cart_item.quantity)
            total_price += item_price

            info = {
                "product_id": cart_item.product.id,
                "size": cart_item.size,
                "price": item_price,
            }
            product_info.append(info)

        cart_data["product_info"] = product_info
        cart_data["total_price"] = total_price
        cart_data["discount"] = 0
        return Response(cart_data)
