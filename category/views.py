from rest_framework import generics
from category.models import Category
from category.serializers import CategorySerializer


class CategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer
    lookup_field = "category_slug"

    def get_queryset(self):
        slug = self.kwargs.get("category_slug")
        return Category.objects.filter(slug=slug)
