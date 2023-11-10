from django.urls import path
from product import views


urlpatterns = [
    path("<slug:slug>/", views.ProductDetail.as_view(), name="product-detail"),
    path("", views.ProductList.as_view(), name="products"),
]
