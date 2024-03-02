from rest_framework import generics

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
