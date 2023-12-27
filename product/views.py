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

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == "SE":
            return Product.objects.filter(seller=self.request.user.seller)
        return Product.objects.all()

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


class CategoryProductView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = ProductCategorySerializer
    lookup_field = "slug"
    lookup_url_kwarg = "category_slug"


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True).prefetch_related(
        "subcategories"
    )
    serializer_class = CategorySerializer
