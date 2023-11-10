from django.urls import path
from product import views


urlpatterns = [
    path("<str:pk>/", views.ProductDetail.as_view(), name="product-detail"),
    path("", views.ProductList.as_view(), name="products"),
]
