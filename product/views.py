from rest_framework import generics, permissions

from product.models import Product
from product.serializers import ProductSerializer
from users.permissions import IsSeller, ReadOnly


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsSeller()]
        return [permissions.AllowAny()]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "slug"
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSeller | ReadOnly]
