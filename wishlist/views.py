from rest_framework import generics

from users.permissions import IsCustomer
from wishlist.models import WishlistItem
from wishlist.serializers import WishListItemSerializer, WishlistItemWriteSerializer


class WishlistItemsView(generics.ListCreateAPIView):
    permission_classes = [IsCustomer]

    def get_queryset(self):
        user = self.request.user
        return WishlistItem.objects.filter(wishlist__customer__user=user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return WishListItemSerializer
        else:
            return WishlistItemWriteSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}


class WishlistItemsUpdateView(generics.DestroyAPIView):
    permission_classes = [IsCustomer]
    lookup_field = "product__slug"  # this will be used for query
    lookup_url_kwarg = "product_slug"  # this will be used in url
    # if both are same then just use : 'lookup_field'

    def get_queryset(self):
        user = self.request.user
        product_slug = self.kwargs["product_slug"]
        return WishlistItem.objects.filter(
            wishlist__customer__user=user, product__slug=product_slug
        )

    def get_serializer_class(self):
        return WishListItemSerializer
