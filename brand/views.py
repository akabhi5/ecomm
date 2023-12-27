from users.permissions import IsSeller
from .models import Brand
from .serializers import BrandProductSerializer, BrandSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny


class BrandListView(ListCreateAPIView):
    serializer_class = BrandSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsSeller()]
        return [AllowAny()]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == "SE":
            return Brand.objects.filter(seller=self.request.user.seller)
        return Brand.objects.all()

    def get_serializer_context(self):
        return {"user": self.request.user}


class BrandView(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsSeller()]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BrandProductSerializer
        return BrandSerializer
