from rest_framework import generics, permissions

from product.models import Product, Category
from product.serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    ProductSerializerRead,
    CategorySerializer,
)
from users.permissions import IsSeller, ReadOnly
from django.db.models import Q


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsSeller()]
        return [permissions.AllowAny()]

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductSerializerRead
        return ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "slug"
    queryset = Product.objects.all()
    permission_classes = [IsSeller | ReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductSerializerRead
        return ProductSerializer


class CategoryProductView(generics.ListAPIView):
    serializer_class = ProductCategorySerializer
    lookup_field = "category_slug"

    def get_queryset(self):
        slug = self.kwargs.get("category_slug")
        return Category.objects.filter(slug=slug)


class CategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.request.GET.get("category_type") == "parent":
            return Category.objects.filter(parent=None)
        return Category.objects.filter(~Q(parent=None))
