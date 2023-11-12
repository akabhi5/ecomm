from rest_framework import generics
from review.serializers import ReviewSerializer
from review.models import Review


class ReviewView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    lookup_field = "product_slug"

    def get_queryset(self):
        product_slug = self.kwargs["product_slug"]
        return Review.objects.filter(product__slug=product_slug)
